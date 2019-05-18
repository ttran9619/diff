#! /usr/bin/env python
# encoding: utf-8
# Thomas Nagy, 2006-2010 (ita)

# the following two variables are used by the target "waf dist"
VERSION = '0.1'
APPNAME = 'diff'

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = 'build'

# --------------------------------------------------------------------------------------------
#                                           OPTIONS
# --------------------------------------------------------------------------------------------


def options(opt):
    import os

    opt.add_option('--mode',
                   action='store',
                   help='Compile Mode (release, debug, profile)',
                   default='auto')
    opt.add_option('--target',
                   action='store',
                   help='Target OS (cygwin,linux,macos)',
                   default='auto')

    opt.load('compiler_c')
    opt.load('compiler_cxx')

# --------------------------------------------------------------------------------------------
#                                          CONFIGURE
# --------------------------------------------------------------------------------------------


def configure(ctx):
    from waflib import Options, Logs
    import subprocess
    import waflib
    import os

    # Determine Operating Environment
    target = Options.options.target
    if target == 'auto':
        if os.name == 'nt':
            target = 'msvc'
        elif 'cygwin_nt' in os.uname()[0].lower():
            target = 'cygwin'
        elif os.uname()[0] == 'Darwin':
            target = 'macos'
        elif os.uname()[0] == 'Linux':
            target = 'linux'

    if target not in ('msvc', 'cygwin', 'linux', 'macos'):
        waflib.Logs.error('Invalid OS "' +
                          target +
                          '", please pass a valid --target=... flag')
        return

    mode = Options.options.mode
    if mode == 'auto':
        mode = 'release'

    if mode not in ('release', 'debug', 'profile'):
        waflib.Logs.error('Invalid mode "' +
                          target +
                          '", please pass a valid --mode=... flag')
        return

    ctx.load('compiler_c')
    ctx.load('compiler_cxx')

    # Compiler Check
    ctx.check_cc(header_name="stdio.h",
                 msg='Checking C compiler works',
                 errmsg="No")

    ctx.check_cxx(header_name="cstdio",
                  msg='Checking C++ compiler works',
                  errmsg="No")

    # MSVC
    if target == 'msvc':
        pass

    # Cygwin
    elif target == 'cygwin':
        pass

    # macOS
    elif target == 'macos':
        pass

    # Linux
    elif target == 'linux':
        pass

    ctx.env['target'] = target
    ctx.env['mode'] = mode

    waflib.Logs.info('Defaults set to target ' +
                     target +
                     ' in ' +
                     mode +
                     ' mode.')


# --------------------------------------------------------------------------------------------
#                                            BUILD
# --------------------------------------------------------------------------------------------


def build(bld):
    from waflib import Options
    import os

    # Grab target and mode configurations
    target = bld.env['target']
    mode = bld.env['mode']

    # Override mode and target if user set options
    if Options.options.mode != 'auto':
        mode = Options.options.mode

    if Options.options.target != 'auto':
        target = Options.options.target

    link_flags = []
    build_flags = []
    build_cc_flags = []
    build_cxx_flags = []
    src_list = []
    inc_paths = []
    lib_list = []
    framework_list = []

    # MSVC
    if target == 'msvc':
        build_flags += ['/W4']
        build_flags += ['/WX']
        build_flags += ['/EHsc']

        build_cxx_flags += ['/std:c++17']
    # GCC-like compilers
    else:
        build_flags += ['-Wall']
        build_flags += ['-Werror']
        build_cxx_flags += ['--std=c++17']

    # Source Files
    src_list += ['src/diff.cpp']

    # Include Paths
    inc_paths += []

    # Set up mode specific configs
    if mode == 'debug':
        build_flags += ['-g', '-DDEBUG=1']
    elif mode == 'profile':
        build_flags += ['-pg']
    elif mode == 'release':
        build_flags += ['-O2']

    # MSVC
    if target == 'msvc':
        pass

    # Cygwin
    elif target == 'cygwin':
        pass

    # macOS
    elif target == 'macos':
        pass

    # Linux
    elif target == 'linux':
        pass

    print('Building ' + APPNAME + ' on ' + target + ' in ' + mode + ' mode.')

    # Build the program
    bld.program(features='c cxx cxxprogram',
                cflags=build_flags + build_cc_flags,
                cxxflags=build_flags + build_cxx_flags,
                linkflags=link_flags,
                source=src_list,
                target=APPNAME,
                lib=lib_list,
                framework=framework_list,
                includes=inc_paths)


# --------------------------------------------------------------------------------------------
#                                            INSTALL
# --------------------------------------------------------------------------------------------


def install(bld):
    target = bld.env['target']
    start_dir = bld.path.find_dir('build')
    install_directory = ''

    # Windows
    if target == 'msvc':
        install_directory = 'C:/bin/'
    # UNIX
    else:
        install_directory = '/usr/local/bin/'

    bld.install_as(start_dir.ant_glob(APPNAME+'*'),
                   install_directory,
                   cwd=start_dir)


# --------------------------------------------------------------------------------------------
#                                          UNINSTALL
# --------------------------------------------------------------------------------------------


def uninstall(bld):
    import os
    import glob

    target = bld.env['target']
    install_directory = ''

    # Windows
    if target == 'msvc':
        install_directory = 'C:/bin/'
    # UNIX
    else:
        install_directory = '/usr/local/bin/'

    for exe in glob.glob(install_directory+APPNAME+'*'):
        os.remove(exe)
