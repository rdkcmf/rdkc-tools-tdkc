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
  <name>sysutil_CheckWifiConnection_AfterReboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to set network configurations in wpa_supplicant.conf file and check the wifi connection status after reboot.</synopsis>
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
    <test_case_id>TC_sysutil_06</test_case_id>
    <test_objective>Test script to set network configurations in wpa_supplicant.conf file and check the wifi connection status after reboot.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-RDKC</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.If the load module status is success, set the network configurations in wpa_supplicant.conf file.
3.Invoke ExecuteCmd function to execute "updateNetworkConfig.sh" script with ssid &amp; psk to be set as its arguments.
4.Reboot the device.
5.When the device comes up, check whether wlan0 is getting IP, to verify wifi connection status.
6.Invoke ExecuteCmd function to execute "updateNetworkConfig.sh" script to revert the network configurations set
7.Update the test result as success / failure based on wifi connection status.</automation_approch>
    <expected_output>wlan0 status should be UP</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_CheckWifiConnection_AfterReboot</test_script>
    <skipped>No</skipped>
    <release_version>M75</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkcConfigParserUtility;
from tdkcConfigParserUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil_tdkc","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'sysutil_CheckWifiConnection_AfterReboot');

#Get the result of connection with test component and RDKC
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parsing device config file to get ssid, psk & tdk_path
    parseStatus = parseDeviceConfig(obj);
    ssid = tdkcConfigParserUtility.ssid
    psk  = tdkcConfigParserUtility.psk
    tdk_path  = tdkcConfigParserUtility.tdk_path
    if (len(ssid.strip()) == 0 or len(psk.strip()) == 0 or len(tdk_path.strip()) == 0):
        print "Error : Empty parameters in device config file : cannot procced"
        exit();
    else:
        ssid.replace("$","\$")
        psk.replace("$","\$")

    print "\nTEST STEP 1 : To set network configurations in wpa_supplicant.conf file"
    print "EXPECTED RESULT : wpa_supplicant.conf should be updated"
    tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
    cmd = "sh " + tdk_path + "updateNetworkConfig.sh \"configure\" \"" + ssid + "\" \"" + psk + "\""
    print "Command to be executed : %s" %(cmd)
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if expectedresult in actualresult:
        cmdOutput = tdkTestObj.getResultDetails();
        print "ACTUAL RESULT  : Command Execution to set network configuration Success"
        print "wpa_supplicant.conf updated successfully\n"
        tdkTestObj.setResultStatus("SUCCESS");

        #Reboot
        obj.initiateReboot();

        print "\nTEST STEP 2 : To get wifi connection status using ifconfig command"
        print "EXPECTED RESULT : wifi connection status should be obtained"
        tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
        expectedresult = "SUCCESS"
        cmd  = "ifconfig wlan0 | grep \"inet addr:\""
        print "Command to be executed : %s" %(cmd)
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            cmdOutput = tdkTestObj.getResultDetails();
            cmdOutput =  str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
            print "ACTUAL RESULT  : Command Execution to get wifi connection info Success"
            print "Value Returned : "
            print(cmdOutput)
            tdkTestObj.setResultStatus("SUCCESS");

            print "\nTEST STEP 3 : To check whether wlan0 interface gets IP or not"
            print "EXPECTED RESULT : wlan0 network should get an IP"
            if "inet addr:" in cmdOutput:
                print "ACTUAL RESULT   : wlan0 network is UP with an IP"
                print "[TEST EXECUTION RESULT] : SUCCESS\n"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print "ACTUAL RESULT   : wlan0 network is DOWN"
                print "[TEST EXECUTION RESULT] : FAILURE\n"
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "ACTUAL RESULT  : Command execution to get wifi connection status Failed"
            print "Value Returned : %s\n" %(cmdOutput)
            tdkTestObj.setResultStatus("FAILURE");

        print "TEST STEP 4 : Revert wpa_supplicant.conf file"
        print "EXPECTED RESULT : Remove the configurations set from wpa_supplicant.conf"
        tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
        cmd = "sh " + tdk_path + "updateNetworkConfig.sh \"revert\""
        print "Command to be executed : %s" %(cmd)
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
            cmdOutput = tdkTestObj.getResultDetails();
            print "ACTUAL RESULT  : Command Execution to revert network configuration Success"
            print "wpa_supplicant.conf updated successfully\n"
            tdkTestObj.setResultStatus("SUCCESS");

            print "\nTEST STEP 5 : To get wpa_supplicant.conf after removing network config details"
            print "EXPECTED RESULT : reverted wpa_supplicant.conf should be obtained"
            tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
            expectedresult = "SUCCESS"
            cmd  = "cat /etc/wpa_supplicant.conf"
            print "Command to be executed : %s" %(cmd)
            tdkTestObj.addParameter("command", cmd);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            if expectedresult in actualresult:
                cmdOutput = tdkTestObj.getResultDetails();
                cmdOutput =  str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
                print "ACTUAL RESULT  : Command Execution to get reverted wpa_supplicant.conf Success"
                print "Value Returned : "
                print(cmdOutput)

                print "\nTEST STEP 6 : To check whether network configurations in wpa_supplicant.conf removed"
                print "EXPECTED RESULT : configurations set should not be available"
                if ssid not in cmdOutput and psk not in cmdOutput:
                    print "ACTUAL RESULT   : network configurations reverted successfully"
                    print "[TEST EXECUTION RESULT] : SUCCESS\n"
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Rebooting the device to reset the network connections"
                    obj.initiateReboot();
                else:
                    print "ACTUAL RESULT   : network configurations not reverted"
                    print "[TEST EXECUTION RESULT] : FAILURE\n"
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print "ACTUAL RESULT  : Command execution to get reverted wpa_supplicant.conf Failed"
                print "Value Returned : %s\n" %(cmdOutput)
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print "ACTUAL RESULT  : Command execution to revert network configuration Failed"
            print "Value Returned : %s\n" %(cmdOutput)
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "ACTUAL RESULT  : Command execution to set network configuration Failed"
        print "Value Returned : %s\n" %(cmdOutput)
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");

