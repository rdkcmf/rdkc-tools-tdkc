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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>sysutil_IsCameraDeviceDetected</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to check whether camera device is detected or not. Checking whether /dev/video0 is available or not.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <test_case_id>TC_sysutil_01</test_case_id>
    <test_objective>Test script to check whether camera device is detected or not. Checking whether /dev/video0 is available or not.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-RDKC</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.If the load module status is success, check whether camera device is detected or not.
3.Invoke ExecuteCmd function to execute the command "ls /dev/video0"
4.From the command output, check whether /dev/video0 file is listed. If file is found, it indicates that camera device is detected.
5.Update the test result as success / failure based on camera device detected status.</automation_approch>
    <expected_output>/dev/video0 should be found.</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_IsCameraDeviceDetected</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil_tdkc","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'sysutil_IsCameraDeviceDetected');

#Get the result of connection with test component and RDKC
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    print "\nTEST STEP 1 : To check whether Camera Device is detected or not"
    print "EXPECTED RESULT : Should get the entry /dev/video0"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    cmd = "ls /dev/video0"
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        cmdOutput = tdkTestObj.getResultDetails();
        cmdOutput = cmdOutput.replace('\\n',"");
        print "ACTUAL RESULT  : Command Execution to detect Camera device success"
        print "Value Returned : %s\n" %(cmdOutput)

        print "TEST STEP 2 : To check whether /dev/video0 is found or not"
        print "EXPECTED RESULT : /dev/video0 should be available"
        if cmdOutput.strip(" ") == "/dev/video0":
            print "ACTUAL RESULT   : /dev/video0 Found : Camera Device detected"            
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "ACTUAL RESULT   : /dev/video0 Not Found : Camera Device not detected"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "ACTUAL RESULT  : Command execution to detect Camera device Failed"
        print "Value Returned : %s\n" %(cmdOutput)
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");
