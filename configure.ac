##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.
dnl AC_PREREQ([2.69])
AC_INIT(tdk-c, 1.0, sugasini@tataelxsi.co.in,tdk-c)
AC_CONFIG_SRCDIR([agent/src/agentmain.cpp])
AM_CONFIG_HEADER(config.h)
AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE([foreign no-dist-gzip dist-bzip2 subdir-objects 1.9])
LT_INIT
dnl subdirectories.
dnl Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_CPP
AC_PROG_CXXCPP
dnl use pretty build output with automake >= 1.11
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])],
  [AM_DEFAULT_VERBOSITY=1
   AC_SUBST(AM_DEFAULT_VERBOSITY)])
dnl **********************************
dnl checks for dependencies
dnl **********************************
AC_HEADER_STDC
dnl Checks for header files.
AC_CHECK_HEADERS([limits.h memory.h stdlib.h string.h sys/socket.h unistd.h])
dnl Checks for typedefs, structures, and compiler characteristics.
dnl AC_CHECK_HEADER_STDBOOL
AC_TYPE_UINT8_T
dnl Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([memset strdup strerror])
COPTS="-DDEBUG_LEVEL_TRACE"
AM_CXXFLAGS="$AM_CXXFLAGS -DDEBUG_LEVEL_TRACE"
AGENT_FLAGS=" "
CONFIG_PREFIX="/etc/"
RDK_VERSION="RDKC"
AC_SUBST(COPTS)
AC_SUBST(AGENT_FLAGS)
AC_SUBST(CONFIG_PREFIX)
AC_SUBST(RDK_VERSION)
AC_CONFIG_FILES([Makefile
	 agent/Makefile
         SystemUtil_tdkc_stub/Makefile
         ])
AC_OUTPUT

