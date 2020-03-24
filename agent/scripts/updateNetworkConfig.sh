#!/bin/sh
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



#------------------------------------------------------------------------------------------------------
# Tool Usage
#------------------------------------------------------------------------------------------------------
usage()
{
    echo -e "\nUsage : sh updateNetworkConfig.sh [action] ssid[username] psk[password]"
    echo -e "Eg    : sh $0 \"configure\" \"AP1\" \"AP_123\""
    echo -e "                  or                      "
    echo -e "      : sh $0 \"revert\"\n"
}


#------------------------------------------------------------------------------------------------------
# Checking Command Line Arguments
#------------------------------------------------------------------------------------------------------
ACTION=""
SSID=""
PSK=""
TDK_PATH="/opt/TDK"
argument_count=$#
if [[ $1 == "configure" && $argument_count == 3 ]]; then
    ACTION="$1"
    SSID="$2"
    PSK="$3"
    echo -e "\nProvided SSID = \"$SSID\" , PSK = \"$PSK\""
elif [[ $1 == "revert" ]]; then
    ACTION="$1"
else
    usage
    exit 0
fi

#------------------------------------------------------------------------------------------------------
# Update Network Configurations
#------------------------------------------------------------------------------------------------------

WPA_CONF="/etc/wpa_supplicant.conf"
WPA_CONF_BACKUP="$TDK_PATH/backup_wpa_supplicant.conf"
if [[ $ACTION == "configure" ]]; then
    file_exist=`ls $WPA_CONF`

    if [[ ! -z $file_exist && $file_exist != " " ]]; then
        cp $WPA_CONF $WPA_CONF_BACKUP
        if [[ $? -eq 0 ]]; then
            echo -e "Taking backup : copied $WPA_CONF to $WPA_CONF_BACKUP"
        else
            echo -e "Taking backup : copy $WPA_CONF to $WPA_CONF_BACKUP failed"
        fi

        echo -e "Updating network configuration in $WPA_CONF"
        ssid_exist=$(awk '/ssid=*/ {print $0}' $WPA_CONF)
        psk_exist=$(awk  '/psk=*/  {print $0}' $WPA_CONF)
        if [[ ! -z $ssid_exist && ! -z $psk_exist ]]; then
            ssid_exist=$(echo $ssid_exist | cut -d "=" -f 2)
            psk_exist=$(echo  $psk_exist  | cut -d "=" -f 2)
             echo -e "Existing SSID = $ssid_exist , PSK = $psk_exist"
            echo -e "over-writing existing network configurations"
            sed -i -E 's/ssid=.+/ssid=\"'"$SSID"'\"/' $WPA_CONF
            sed -i -E 's/psk=.+/psk=\"'"$PSK"'\"/'    $WPA_CONF
        else
            echo -e "writing new network configurations"
            echo -e "network={\nssid=\"$SSID\"\npsk=\"$PSK\"\n}" >> $WPA_CONF
        fi

        echo -e "\nCurrent data in $WPA_CONF:"
        cat $WPA_CONF
    else
        echo "$WPA_CONF file not found"
    fi
elif [[ $ACTION == "revert" ]]; then
    file_exist=`ls $WPA_CONF_BACKUP`
    if [[ ! -z $file_exist && $file_exist != " " ]]; then
        file_exist=`ls $WPA_CONF`
        if [[ ! -z $file_exist && $file_exist != " " ]]; then
            cp $WPA_CONF_BACKUP $WPA_CONF
            if [[ $? -eq 0 ]]; then
                echo -e "Network configurations in $WPA_CONF reverted successfully"
            else
                echo -e "$WPA_CONF Network configurations revert failed"
            fi
            echo -e "\nCurrent data in $WPA_CONF:"
            cat $WPA_CONF
        else
            echo "$WPA_CONF file not found to revert the Network configurations"
        fi
    else
        echo $WPA_CONF_BACKUP file not found
    fi
fi


