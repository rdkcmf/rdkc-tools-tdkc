/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2020 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
#ifndef __SysUtil_STUB_H__
#define __SysUtil_STUB_H__
#include <json/json.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <algorithm>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#define IN
#define OUT
#define BUFF_LENGTH 512
#define TEST_SUCCESS true
#define TEST_FAILURE false
using namespace std;
class RDKTestAgent;
class SystemUtilAgent : public RDKTestStubInterface, public AbstractServer<SystemUtilAgent>
{
        public:
               SystemUtilAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <SystemUtilAgent>(ptrRpcServer)
               {
                   this->bindAndAddMethod(Procedure("TestMgr_ExecuteCmd", PARAMS_BY_NAME, JSON_STRING,"command",JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_ExecuteCmd);
                   this->bindAndAddMethod(Procedure("TestMgr_BasicFunction", PARAMS_BY_NAME, JSON_STRING,NULL), &SystemUtilAgent::SystemUtilAgent_BasicFunction);
               }
                /*Inherited functions*/
                bool initialize(IN const char* szVersion);
                bool cleanup(const char*);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();
		void SystemUtilAgent_ExecuteCmd(IN const Json::Value& req, OUT Json::Value& response);
                void SystemUtilAgent_BasicFunction(IN const Json::Value& req, OUT Json::Value& response);
};
#endif

