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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>sysutil_IsCameraDeviceStreaming</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to check whether camera device is streaming or not using rms logs</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>TC_sysutil_07</test_case_id>
    <test_objective>Test Script to check whether camera device is streaming or not using rms logs</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-C</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.If the load module status is success, set the resolution and room id details in rms.conf and uncomment file append section to enable rms logging in config.lua file
3.Reboot the device
4.Check whether camera device is streaming or not using rms.log file
6.Update the test status if rms.log has expected patterns
5.Revert the changes in rms.conf and config.lua
6.Unload systemutil_tdkc  module</automation_approch>
    <expected_output>rms.log file should have gst_InitFrame SUCCESS and Inbound connection accepted pattens.</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_IsCameraDeviceStreaming</test_script>
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
import time
 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil_tdkc","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'sysutil_IsCameraDeviceStreaming');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parsing device config file
    parseStatus = parseDeviceConfig(obj);
    print "\nTEST STEP 1 : Update resolution settings & room ID in rms.conf file and enable rms logging"
    print "EXPECTED RESULT : rms.conf should have required resolution,room ID & config.lua file append section should be uncommented"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    tdk_path  = tdkcConfigParserUtility.tdk_path
    cmd = "sh " + tdk_path + "updateRMSConf.sh \"configure\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        cmdOutput = tdkTestObj.getResultDetails();
        print "rms.conf & config.lua updated successfully"
        print "ACTUAL RESULT  : Command Execution to update resolutions,room ID in rms.conf & enable rms logging Success\n"
        tdkTestObj.setResultStatus("SUCCESS");

        #Reboot
        obj.initiateReboot();
        time.sleep(120);

        print "\n TEST STEP2: Check whether the camera device is streaming or not using rms log"
        print "EXPECTED RESULT : Should get log prints gst_InitFrame SUCCESS & Inbound connection accepted"
        tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
        expectedresult = "SUCCESS"
        data1 = "gst_InitFrame SUCCESS"
        data2 = "Inbound connection accepted"
        cmd = "awk '/" + data1 + "/{init=$0;next} /" + data2 + "/{print init \"\\n\" $0;exit}' /opt/logs/rms.*.log"
        print "Command to be executed : %s" %(cmd)
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            cmdOutput = tdkTestObj.getResultDetails();
            cmdOutput = str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
            print "Value Returned : "
            print cmdOutput
            if data1 and data2 in cmdOutput:
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT : camera device is streaming properly"
                print "[TEST EXECUTION RESULT ] : SUCCESS\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "ACTUAL RESULT : camera device is not streaming properly"
                print "[TEST EXECUTION RESULT ] : FAILURE\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "ACTUAL RESULT : Not able to check whether camera device is streaming or not"
            print "[TEST EXECUTION RESULT ] : FAILURE\n"

        print "\nTEST STEP 3 : Revert the configurations in rms.conf and disable rms logging"
        print "EXPECTED RESULT : rms.conf should be reverted & config.lua file append section should be commented"
        tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
        tdk_path  = tdkcConfigParserUtility.tdk_path
        cmd = "sh " + tdk_path + "updateRMSConf.sh \"revert\""
        print "Command to be executed : %s" %(cmd)
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            cmdOutput = tdkTestObj.getResultDetails();
            tdkTestObj.setResultStatus("SUCCESS");
            print "rms.conf & config.lua reverted successfully"
            print "ACTUAL RESULT  : Command Execution to revert configurations in rms.conf & disable rms logging Success"
            print "[TEST EXECUTION RESULT ] : SUCCESS\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Value Returned : %s\n" %(cmdOutput)
            print "ACTUAL RESULT  : Command Execution to revert configurations in rms.conf & disable rms logging Failed"
            print "[TEST EXECUTION RESULT ] : FAILURE\n"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Value Returned : %s\n" %(cmdOutput)
        print "ACTUAL RESULT  : Command execution to set resolution ,room ID in rms.conf & enable rms logging Failed"
        print "[TEST EXECUTION RESULT ] : FAILURE\n"

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
