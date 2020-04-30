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
  <name>sysutil_WEBUI_WEBRTCDemo_LiveStreamMultiBrowser</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to play live stream in multiple browser simultaneously</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <test_case_id>TC_sysutil_11</test_case_id>
    <test_objective>Test Script to play live stream in multiple browser simultaneously</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-C</test_setup>
    <pre_requisite>TDK agent should be running in the device and device should be online in Test Manager.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Load the systemutil_tdkc module.
2.Update network info in wpa_supplicant file
3.add resolution, room id info in rms.conf and uncomment file append section to enable rms logging in config.lua file
4.Reboot the device
5.Check the wifi connection and camera streaming status
6.start hub, node and launch the webrtc demo url in two browsers
7.update RRS info in both demo page and check whether it is updated properly
8.click on the play button in both UI
9.check rms.log whether required patterns are available
11.Update the test result based on play status
11.revert wifi and rms conf files and unload the module</automation_approch>
    <expected_output>After clicking on the play button, Client joined, WebRTC connection started ,DTLS handshake is 1  patterns should be available in rms.log.</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_WEBUI_WEBRTCDemo_LiveStreamMultiBrowser</test_script>
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
from tdkcUtility import *;
import tdkcUtility


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil_tdkc","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'sysutil_WEBUI_WEBRTCDemo_LiveStreamMultiBrowser');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('BasicFunction_TDKC');
    tdkTestObj.executeTestCase(expectedresult);

    #Parsing device config file
    parseStatus = parseDeviceConfig(obj);
    ssid = tdkcConfigParserUtility.ssid
    psk  = tdkcConfigParserUtility.psk
    wifiConnStatus  = "FALSE"
    camStreamStatus = "FALSE"

    #Setting pre-requisites : configuration for wifi-connection
    wifiConfStatus = tdkcUtility.updateWIFIConf(obj,ssid,psk)

    #Setting pre-requisites : configuration for rms
    rmsConfStatus  = tdkcUtility.updateRMSConf(obj);

    #Reboot the device and check wifi and camera streaming status
    if expectedresult in wifiConfStatus and expectedresult in rmsConfStatus:
        #Reboot
        obj.initiateReboot();
        time.sleep(120);
        wifiConnStatus  = tdkcUtility.isConnectedToWIFI(obj)
        camStreamStatus = tdkcUtility.isCameraStreaming(obj)

    #Launch WEBRTC Demo page and play video stream
    if wifiConnStatus == "TRUE" and camStreamStatus == "TRUE":
        #Set Selenium grid
        print "\nTEST STEP : Start selenium Hub, Node and launch the URL in browser"
        print "EXPECTED RESULT : selenium Hub & Node should be started, URL should be opened in browser"
        webrtcDemoURL = tdkcConfigParserUtility.webrtcDemoURL
        UICheckXpath = tdkcConfigParserUtility.UICheckXpath
        UICheckData = tdkcConfigParserUtility.UICheckData
        driver1,status1 = tdkcWEBUIUtility.startSeleniumGrid(tdkTestObj,webrtcDemoURL,UICheckXpath,UICheckData,"NoLogin");
        if status1 == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT : selenium Hub & Node started , URL opened in browser1 successfully\n"

            status2,driver2 = openLocalWebUI(tdkTestObj,webrtcDemoURL,"NoLogin",UICheckXpath,UICheckData);
            if status2 == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS");
                print "ACTUAL RESULT : selenium Hub & Node started , URL opened in browser2 successfully\n"

                status1 = tdkcUtility.updateWEBRTCDemoPage(driver1);
                status2 = tdkcUtility.updateWEBRTCDemoPage(driver2);
                if status1 == "SUCCESS" and status2 == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "\nTEST STEP : Start playing video stream by clicking the play button in both browser"
                    print "EXPECTED RESULT : Play button should be clicked to start the video"
                    status1 = tdkcWEBUIUtility.playStreamInWEBUI(driver1);
                    status2 = tdkcWEBUIUtility.playStreamInWEBUI(driver2);
                    if status1 == "SUCCESS" and status2 == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "ACTUAL RESULT : Started playing video stream in both browsers successfully"

                        time.sleep(60)
                        print "\nTEST STEP: check whether video is playing or not, using rms & browser logs"
                        print "EXPECTED RESULT : Should get Client joined,WebRTC connection started & DTLS handshake is 1"
                        tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
                        expectedresult = "SUCCESS"
                        data1="Client joined"
                        data2="WebRTC connection started"
                        data3="DTLS handshake is 1"
                        data4 = "Video added"
                        cmd = "awk '/" + data1 + "/{print $0} /" + data2 + "/{print $0} /" + data3 + "/{print $0}' /opt/logs/rms.*.log"
                        print "Command to be executed : %s" %(cmd)
                        tdkTestObj.addParameter("command", cmd);
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        status1,msg1 = tdkcWEBUIUtility.getDebugMsgInWEBUI(driver1);
                        status2,msg2 = tdkcWEBUIUtility.getDebugMsgInWEBUI(driver2);
                        if expectedresult in actualresult and expectedresult in status1 and expectedresult in status2:
                            cmdOutput = tdkTestObj.getResultDetails();
                            cmdOutput = str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
                            print "Value Returned : "
                            print cmdOutput
                            print "Browser1 logs  : "
                            print msg1
                            print "Browser2 logs  : "
                            print msg2
                            if data1 and data2 and data3 in cmdOutput and data4 in msg1 and data4 in msg2:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "ACTUAL RESULT : video is playing properly in web UI"
                                print "[TEST EXECUTION RESULT :SUCCESS]\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "ACTUAL RESULT : video is not playing properly in web UI"
                                print "[TEST EXECUTION RESULT ] : FAILURE\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "ACTUAL RESULT : Not able to check whether video is playing or not"
                            print "[TEST EXECUTION RESULT ] : FAILURE\n"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "ACTUAL RESULT : Playing video stream in browsers failed"
                        print "[TEST EXECUTION RESULT ] : FAILURE\n"
                else:
                    tdkTestObj.setResultStatus("FAILURE");

                driver2.quit();
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set selenium grid and launch the WEBRTC Demo URL in browser2"
                print "[TEST EXECUTION RESULT ] : FAILURE\n"

            driver1.quit();
            #Kill selenium hub and node
            print "Kill selenium hub and node"
            status = tdkcWEBUIUtility.kill_hub_node()
            if status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: WebUI post-requisite set successfully\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: WebUI post-requisite not set\n"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to set selenium grid and launch the WEBRTC Demo URL in browser1"
            print "[TEST EXECUTION RESULT ] : FAILURE\n"

    #Setting post-requisite : disconnect wifi & revert rms conf
    if expectedresult in wifiConfStatus and expectedresult in rmsConfStatus:
        revertWIFIConfStatus = tdkcUtility.revertWIFIConf(obj);
        revertRMSConfStatus  = tdkcUtility.revertRMSConf(obj);

        if expectedresult in revertWIFIConfStatus and expectedresult in revertRMSConfStatus:
            print "Rebooting the device to reset the network connections & rms conf ..."
            obj.initiateReboot();

    obj.unloadModule("systemutil_tdkc");
else:
    print "Failed to load the module";
    obj.setLoadModuleStatus("FAILURE");


