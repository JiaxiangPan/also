#!/usr/bin/env python3
import os
import subprocess
import sys

from jinja2 import Environment

#inspired from EPFL Cirkit Tool, Dr. Mathias Soeken

header = """/* also: Advanced Logic Synthesis and Optimization tool
 * Copyright (C) 2019- Ningbo University, Ningbo, China 
 * 
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */
"""

env = Environment()
header_template = env.from_string('''
{{ header }}
/**
 * @file {{ basename }}.hpp
 *
 * @brief TODO
 *
 * @author {{ author }}
 * @since  0.1
 */

#ifndef {{ basename.upper() }}_HPP
#define {{ basename.upper() }}_HPP

namespace {{ namespace }}
{



}

#endif

''')

source_template = env.from_string('''
{{ header }}
#include "{{ basename }}.hpp"

namespace also
{

/******************************************************************************
 * Types                                                                      *
 ******************************************************************************/

/******************************************************************************
 * Private functions                                                          *
 ******************************************************************************/

/******************************************************************************
 * Public functions                                                           *
 ******************************************************************************/

}

''')

def git_user_name():
    return subprocess.check_output( ["git", "config", "--global", "user.name"] ).decode( "utf-8" ).strip()

#def make_header( header, basename, author ):
 #   return header_template.render( header = header, basename = basename, author = author ).strip()

def make_header( header, basename, namespace, author ):
    return header_template.render( header = header, basename = basename, namespace = namespace, author = author ).strip()

def make_source( header, basename ):
    return source_template.render( header = header, basename = basename ).strip()

if __name__ == "__main__":
    argc = len( sys.argv )
    if argc == 1 or argc > 5:
        print( "usage: ./utils/make_src_file.py filename [subdir [filetype [author]]]" )
        print( "example: ./utils/make_src_file.py test src/mig hpp Zhufei" )
        exit( 1 )

    name     = sys.argv[1]
    subdir   = sys.argv[2] if argc > 2 else "."
    filetype = sys.argv[3] if argc > 3 else "both"
    author   = sys.argv[4] if argc > 4 else git_user_name()

    basename = os.path.basename( name )

    pathname = "./" if subdir == "." else "%s" % subdir
    #pathname = pathname + "src/" + os.path.dirname( name )
    if not os.path.isdir( pathname ):
        os.makedirs( pathname )
    filename = pathname + "/" + basename

    if filetype == "hpp":
        namespace = "alice"
        with open( filename + ".hpp", "w" ) as f:
            f.write( make_header( header, basename, namespace, author ) + "\n" )
    else:
        namespace = "also"
        with open( filename + ".hpp", "w" ) as f:
            f.write( make_header( header, basename, namespace, author ) + "\n" )

        with open( filename + ".cpp", "w" ) as f:
            f.write( make_source( header, basename ) + "\n" )

    os.system( "cmake build" )
