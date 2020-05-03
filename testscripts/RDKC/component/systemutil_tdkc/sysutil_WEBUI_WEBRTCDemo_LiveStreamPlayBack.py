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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>sysutil_WEBUI_WEBRTCDemo_LiveStreamPlayBack</name>
  <primitive_test_id/>
  <primitive_test_name>ExecuteCmd_TDKC</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test script to perform play back on streamed video content in WEBRTC Demo page</synopsis>
  <groups_id/>
  <execution_time>0</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-C</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKC</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_sysutil_10</test_case_id>
    <test_objective>Test script to perform play back on streamed video content in WEBRTC Demo page</test_objective>
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
6.start hub, node and launch the webrtc demo url in browser
7.update RRS info in demo page and check whether it is updated properly
8.click on the play button
9.check rms.log whether required patterns are available
10.If play is success, click on stop and check for required patterns
11.Update the test result based on playback status
12.revert wifi and rms conf files and unload the module</automation_approch>
    <expected_output>After clicking on the play button, Client joined, WebRTC connection started ,DTLS handshake is 1  patterns should be available in rms.log. Also after clicking stop button RMS stopped streaming to client should be available.</expected_output>
    <priority>High</priority>
    <test_stub_interface>systemutil_tdkc</test_stub_interface>
    <test_script>sysutil_WEBUI_WEBRTCDemo_LiveStreamPlayBack</test_script>
    <skipped>No</skipped>
    <release_version>M76</release_version>
    <remarks/>
  </test_cases>
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
obj.configureTestCase(ip,port,'sysutil_WEBUI_WEBRTCDemo_PlayLiveStream');

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
        driver,status = tdkcWEBUIUtility.startSeleniumGrid(tdkTestObj,webrtcDemoURL,UICheckXpath,UICheckData,"NoLogin");
        if status == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print "ACTUAL RESULT : selenium Hub & Node started , URL opened in browser successfully\n"

            status = tdkcUtility.updateWEBRTCDemoPage(driver);
            if status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS");
                print "\nTEST STEP : Start playing video stream by clicking the play button in UI"
                print "EXPECTED RESULT : Play button should be clicked to start the video"
                status = tdkcWEBUIUtility.playStreamInWEBUI(driver);
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "ACTUAL RESULT : Started playing video stream in UI successfully"

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
                    status,msg = tdkcWEBUIUtility.getDebugMsgInWEBUI(driver);
                    if expectedresult in actualresult and expectedresult in status:
                        cmdOutput = tdkTestObj.getResultDetails();
                        cmdOutput = str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
                        print "Value Returned : "
                        print cmdOutput
                        print "Browser logs  : "
                        print msg
                        if data1 and data2 and data3 in cmdOutput and data4 in msg:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "ACTUAL RESULT : video is playing properly in web UI"
                            print "[TEST EXECUTION RESULT :SUCCESS]\n"

                            print "\nTEST STEP : Stop playing video stream by clicking the stop button in UI"
                            print "EXPECTED RESULT : Stop button should be clicked to stop the video"
                            status = tdkcWEBUIUtility.stopStreamInWEBUI(driver);
                            if status == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "ACTUAL RESULT : Stopped playing video stream in UI successfully"

                                time.sleep(60);
                                print "\nTEST STEP : check whether video is stopped or not, using rms log"
                                print "EXPECTED RESULT : Should get RMS stopped streaming to client "
                                tdkTestObj = obj.createTestStep('ExecuteCmd_TDKC');
                                expectedresult = "SUCCESS"
                                data1="RMS stopped streaming to client"
                                cmd = "awk '/" + data1 + "/{print $0}' /opt/logs/rms.*.log"
                                print "Command to be executed : %s" %(cmd)
                                tdkTestObj.addParameter("command", cmd);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                if expectedresult in actualresult:
                                    cmdOutput = tdkTestObj.getResultDetails();
                                    cmdOutput = str(cmdOutput).replace('\\n',"\n").replace("\\\"","\"")
                                    print "Value Returned : "
                                    print cmdOutput
                                    if data1 in cmdOutput:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "ACTUAL RESULT : video is stopped properly in web UI"
                                        print "[TEST EXECUTION RESULT :SUCCESS]\n"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "ACTUAL RESULT : video is not stopped properly in web UI"
                                        print "[TEST EXECUTION RESULT ] : FAILURE\n"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "ACTUAL RESULT : Not able to check whether video is stopped or not"
                                    print "[TEST EXECUTION RESULT ] : FAILURE\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "ACTUAL RESULT : Stopping video stream in UI failed\n"
                                print "[TEST EXECUTION RESULT ] : FAILURE\n"
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
                    print "ACTUAL RESULT : Playing video stream in UI failed"
                    print "[TEST EXECUTION RESULT ] : FAILURE\n"
            else:
                tdkTestObj.setResultStatus("FAILURE");

            #Kill web-driver
            driverQuitStatus = tdkcWEBUIUtility.kill_web_driver(driver)

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
            print "Failed to set selenium grid and launch the WEBRTC Demo URL"
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



