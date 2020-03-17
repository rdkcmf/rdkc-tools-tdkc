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
#include "SystemUtil_tdkc_stub.h"
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string SystemUtilAgent::testmodulepre_requisites()
{
	return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool SystemUtilAgent::testmodulepost_requisites()
{
	return true;
}
/**************************************************************************
Function name : SystemUtilAgent::initialize
Arguments     : Input arguments are Version string and SystemUtilAgent obj ptr
Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool SystemUtilAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent Initialize----->Entry\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent Initialize----->Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
Function name : SystemUtilAgent::SystemUtilAgent_ExecuteCmd
Arguments     : Input arguments are json request object and json response object
Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
void SystemUtilAgent::SystemUtilAgent_ExecuteCmd(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteCmd -->Entry\n");
	
	FILE *fp = NULL;
        string result = "";
	char buffer[BUFF_LENGTH] = { '\0' };

	/*Frame the command  */
	string cmd = req["command"].asCString();
	DEBUG_PRINT(DEBUG_TRACE, "Command going to be executed : %s\n",cmd.c_str());

	fp = popen(path.c_str(),"r");
	/*Check for popen failure and get the command output*/
	if(fp == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "popen() failure";
		DEBUG_PRINT(DEBUG_ERROR, "popen() failure\n");
		return;
	}
	while(!feof(fp))
	{
                if(fgets(buffer,BUFF_LENGTH,fp) != NULL)
                    result += buffer;
	}
	pclose(fp);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nCommand Output: %s\n",result.c_str());
	response["result"] = "SUCCESS";
	response["details"] = result;
	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
	DEBUG_PRINT(DEBUG_TRACE, "SystemUtilAgent_ExecuteCmd -->Exit\n");
	return;
}

/**************************************************************************
Function Name   : CreateObject
Arguments       : NULL
Description     : This function is used to create a new object of the class "SystemUtilAgent".
 **************************************************************************/
extern "C" SystemUtilAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating SysUtil Agent Object\n");
	return new SystemUtilAgent(ptrtcpServer);
}
/**************************************************************************
Function Name   : cleanup
Arguments       : NULL
Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool SystemUtilAgent::cleanup(IN const char* szVersion)
{
        DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
	return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject
Arguments     : Input argument is SystemUtilAgent Object
Description   : This function will be used to destory the SystemUtilAgent object.
 **************************************************************************/
extern "C" void DestroyObject(SystemUtilAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying SystemUtilAgent object\n");
	delete stubobj;
}
