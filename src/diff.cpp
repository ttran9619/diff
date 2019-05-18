#include <iostream>
#include <filesystem>
#include <unordered_set>
#include <utility>
#include <set>
#include <string>

int main
    (
    const int aArgmentCount,
    char** const aArgumentList
    )
{
    if( aArgmentCount != 3 )
    {
        std::cerr << "Expected 2 arguments, got " << std::to_string( aArgmentCount - 1 ) << std::endl;
        return -1;
    }

    try
    {
        // Find paths in each directory
        const auto pairOfSetsOfPaths = [&]
        {
            const auto generateSetOfPaths = []( const auto& aPath )
            {
                auto ret = std::unordered_set<std::string>{};

                const auto parentPathString = aPath.u8string();
                for( const auto& directoryEntry : std::filesystem::recursive_directory_iterator( aPath ) )
                {
                    ret.insert( directoryEntry.path().u8string().substr( parentPathString.size() ) );
                }

                return ret;
            };

            const auto firstDirectoryPath = std::filesystem::path{ aArgumentList[1] };
            const auto setOfPathsInFirst = generateSetOfPaths( firstDirectoryPath );

            const auto secondDirectoryPath = std::filesystem::path{ aArgumentList[2] };
            const auto setOfPathsInSecond = generateSetOfPaths( secondDirectoryPath );

            return std::make_pair( setOfPathsInFirst, setOfPathsInSecond );
        }();


        // Find unique items in each set
        const auto pairOfSetsOfUniquePaths = [&pairOfSetsOfPaths]
        {
            const auto generateSortedDifferenceSet = []( const auto& aSet1, const auto& aSet2 )
            {
                auto ret = std::set<std::string>{};

                for( const auto& path : aSet1 )
                {
                    if( aSet2.find( path ) == aSet2.end() )
                    {
                        ret.insert( path );
                    }
                }

                return ret;
            };

            const auto uniquePathsInFirst = generateSortedDifferenceSet( pairOfSetsOfPaths.first, pairOfSetsOfPaths.second );
            const auto uniquePathsInSecond = generateSortedDifferenceSet( pairOfSetsOfPaths.second, pairOfSetsOfPaths.first );

            return std::make_pair( uniquePathsInFirst, uniquePathsInSecond );
        }();


        // Print Unique Items
        {
            const auto printItems = []( const auto& aContainer, const auto& aContainerName )
            {
                std::cout << "Unique in " << aContainerName << ":" << std::endl;
                for( const auto& string : aContainer )
                {
                    std::cout << "  " << string << std::endl;
                }
            };

            printItems( pairOfSetsOfUniquePaths.first, aArgumentList[1] );
            printItems( pairOfSetsOfUniquePaths.second, aArgumentList[2] );
        }

    }
    catch( const std::exception& aException )
    {
        std::cerr << aException.what() << std::endl;
    }

    return 0;
}