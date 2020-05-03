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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>sysutil_WEBUI_WEBRTCDemo_IsUIAccessible</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>BasicFunction_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to check whether webrtc demo page is accessible</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-C</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKC</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_sysutil_08</test_case_id>
    <test_objective>Test script to check whether webrtc demo page is accessible</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-C</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.If the load module status is success,start hub, node and launch the webrtc demo url in browser
3.check whether web UI has required data in its header
3.Update the test status as success, if hub,node and demo url is launched successfully in browser.
4.Unload systemutil_tdkc  module</automation_approch>
    <expected_output>webrtc demo page should be opened in browser</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_WEBUI_WEBRTCDemo_IsUIAccessible</test_script>
    <skipped>No</skipped>
    <release_version>M76</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import tdkcConfigParserUtility;
from tdkcConfigParserUtility import *;
import tdkcWEBUIUtility
from tdkcWEBUIUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil_tdkc","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'sysutil_WEBUI_WEBRTCDemo_IsUIAccessible');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parsing device config file
    parseStatus = parseDeviceConfig(obj);
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('BasicFunction_TDKC');
    tdkTestObj.executeTestCase(expectedresult);

    #Set Selenium grid 
    print "\nTEST STEP1 : Start selenium Hub, Node and launch the WEBRTC demo URL in browser"
    print "EXPECTED RESULT : selenium Hub & Node should be started, URL should be accesible & opened in browser"
    webrtcDemoURL = tdkcConfigParserUtility.webrtcDemoURL
    UICheckXpath  = tdkcConfigParserUtility.UICheckXpath
    UICheckData   = tdkcConfigParserUtility.UICheckData
    driver,status = tdkcWEBUIUtility.startSeleniumGrid(tdkTestObj,webrtcDemoURL,UICheckXpath,UICheckData,"NoLogin");
    if status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print "ACTUAL RESULT : selenium Hub & Node started , WEBRTC demo URL is accessible & opened in browser successfully"
        print "[TEST EXECUTION RESULT] : SUCCESS\n"

        #Kill web-driver
        driverQuitStatus = tdkcWEBUIUtility.kill_web_driver(driver);

        #Kill selenium hub and node
        print "Kill selenium hub and node"
        status = tdkcWEBUIUtility.kill_hub_node()
        if "SUCCESS" in status and driverQuitStatus == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print "SUCCESS: WebUI post-requisite set successfully\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: WebUI post-requisite not set\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "ACTUAL RESULT : Failed to set selenium grid & launch the WEBRTC demo URL in browser"
        print "[TEST EXECUTION RESULT] : FAILURE\n"

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
