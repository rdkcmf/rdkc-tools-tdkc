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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>sysutil_IsV4L2ModuleEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to check whether v4l2 module is enabled or not. Checking whether lsmod listing bcm2835_v4l2 module.</synopsis>
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
    <test_case_id>TC_sysutil_04</test_case_id>
    <test_objective>Test script to check whether v4l2 module is enabled or not. Checking whether lsmod listing bcm2835_v4l2 module.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-RDKC</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.If the load module status is success, check whether v4l2 module is enabled or not.
3.Invoke ExecuteCmd function to execute the command "lsmod | grep v4l2"
4.From the command output, check whether bcm2835_v4l2 module loaded or not.
5.Update the test result as success / failure based on bcm2835_v4l2 module load status.</automation_approch>
    <expected_output>lsmod should list v4l2 modules</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_IsV4L2ModuleEnabled</test_script>
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
obj.configureTestCase(ip,port,'sysutil_IsV4L2ModuleEnabled');

#Get the result of connection with test component and RDKC
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    print "\nTEST STEP 1 : To check whether v4l2 module is enabled/loaded or not"
    print "EXPECTED RESULT : Should get the list of v4l2 modules from lsmod"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    #cmd = "lsmod | grep ^\"\<bcm2835_v4l2\>\""
    cmd = "lsmod | grep v4l2 | tr '\\n' ';'"
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        cmdOutput = tdkTestObj.getResultDetails();
        cmdOutput = cmdOutput.replace('\\n',"");
        print "ACTUAL RESULT  : Command Execution v4l2 load module status success"
        print "Value Returned : "
        for module in cmdOutput.split(';'):
            print module

        print "TEST STEP 2 : To check whether bcm2835_v4l2 loaded or not"
        print "EXPECTED RESULT : bcm2835_v4l2 entry should be available"
        if "bcm2835_v4l2" in cmdOutput.strip(" "):
            print "ACTUAL RESULT   : v4l2 Module Enabled/Loaded"
            print "[TEST EXECUTION RESULT] : SUCCESS\n"
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print "ACTUAL RESULT   : v4l2 Module Disabled"
            print "[TEST EXECUTION RESULT] : FAILURE\n"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "ACTUAL RESULT  : Command execution to check v4l2 load module status Failed"
        print "Value Returned : %s\n" %(cmdOutput)
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");

