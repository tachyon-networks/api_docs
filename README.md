

# Welcome to the Tachyon Networks API!

This repo contains the swagger-based docs for the Tachyon Networks Public API routes.  

### Usage & Examples

* Usage tips and details on the <a href="https://tachyon-networks.freshdesk.com/support/solutions/articles/67000659777-tna-30x-restful-api">Tachyon Support Site</a>
* Some <a href="https://github.com/tachyon-networks/api_docs/tree/master/_examples">example python scripts</a> (such as bulk firmware upgrade) can be found in this repo in the "_examples" folder.

<br/>

## API Specs

<table>
<tr> <td colspan="6"> <br/> <img width="70px" src="https://tachyon-networks.com/img/github/tna_github.png"/> 
  <br><b> TNA-30x Product family</b> (60GHz wireless)  <br/> <br/></td></tr>

<tr> 
<td><b>Version</b></td>
<td><b>Date</b></td>
<td><b>Firmware</b></td>
<td><b>Swagger Docs</b></td>
<td><b>Config Key Schema</b></td>
<td><b>Notes </b></td>
</tr>

<tr> 
<td>1.0.7 </td>
<td>Jun 30, 2025 </td>
<td>v1.12.2+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.7/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.7/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support the TNA-303L-65 2.4 management radio.  Radio name was also added to the wireless peer stats output. </td>
</tr>

<tr> 
<td>1.0.6 </td>
<td>Jan 17, 2025 </td>
<td>v1.12.1+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.6/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.6/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support changes in data VLAN protcols, updated failover thresholds, SNMP uptime settings, HTTP server controls, and signal LED controls. Wireless peer ipv4, ipv6, and target RSSI has been added to wireless stats output; device uptime has been added to system stats.</td>
</tr>

<tr> 
<td>1.0.5 </td>
<td>May 17, 2024, (updated Aug 8) </td>
<td>v1.12.0+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.5/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.5/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support alt. local IP, new antenna kits, RADIUS auth, new DHCP option 82 settings, and changes in mgmt VLAN settings. </td>
</tr>

<tr> 
<td>1.0.4 </td>
<td>Jan 9, 2024 </td>
<td>v1.11.4+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.4/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.4/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support ptp mode, max fdb, & disable eth1 data. </td>
</tr>

<tr> 
<td>1.0.3 </td>
<td>Dec 15, 2023 </td>
<td>v1.11.3+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.3/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.3/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support advanced time zones and TNA-303X antenna kits.  Antenna kit is also added to stats output. </td>
</tr>

<tr> 
<td>1.0.2 </td>
<td>July 9, 2023 </td>
<td>v1.11.2+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.2/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.2/keys.html">Config keys</a> </td>
<td>New keys have been added to the config schema to support failover and station SSID profiles.  The output of some of the stats has been expanded upon (discovery/device info added to wireless peers, and bootbank firmware versions added to system stats). </td>
</tr>

<tr> 
<td>1.0.1 </td>
<td>Mar. 13, 2023 </td>
<td>v1.11.1+</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.0/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.1/keys.html">Config keys</a> </td>
<td> New configuration keys have been added to the config schema to support traffic shaping. </td>
</tr>

<tr> 
<td>1.0.0 </td>
<td>Jan. 9, 2023 </td>
<td>v1.11.0</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.0/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.0/keys.html">Config keys</a> </td>
<td></td>
</tr>

<tr> 
<td><1.0.0 </td>
<td>Oct. 1, 2022 </td>
<td>v1.10.x</td>
<td><a href="https://tachyon-networks.github.io/api_docs/tna_30x/v1.0.0/" target="_blank">API routes</a></td>
<td>n/a </td>
<td>API support is limited to the following routes:  /login, /update, /reboot, & /stats, and configuration is not supported.</td>
</tr>

  </table>
<table>
<tr> <td colspan="6"><br/><img width="50px" src="https://tachyon-networks.com/img/sw_small.png"/>  <br><b>TNS-100 Product family</b> (PoE switches) <br/> <br/></td></tr>

<tr> 
<td><b>Version</b></td>
<td><b>Date</b></td>
<td><b>Firmware</b></td>
<td><b>Swagger Docs</b></td>
<td><b>Config Key Schema</b></td>
<td><b>Notes </b></td>
</tr>

<tr> 
<td>1.0.2</td>
<td>Aug 8, 2024 </td>
<td>v1.12.5+ </td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.2/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.2/keys.html">Config keys</a> </td>
<td>Config keys have been updated for changes in VLAN policies and support for new keys for RADIUS auth & adv. timezones settings. </td>
</tr>


<tr> 
<td>1.0.1</td>
<td>Jan 5, 2024 </td>
<td>v1.12.3+ </td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.1/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.1/keys.html">Config keys</a> </td>
<td>Config keys have been updated to support new max VLAN count of 128 and to add support for basic STP.</td>
</tr>

<tr> 
<td>1.0.0</td>
<td>Aug 30, 2023 </td>
<td>v1.12.2+ </td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.0/" target="_blank">API routes</a></td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.0/keys.html">Config keys</a> </td>
<td>Configuration routes are now supported. </td>
</tr>

<tr> 
<td><1.0.0</td>
<td>May. 30, 2023 </td>
<td>v1.12.0+ </td>
<td><a href="https://tachyon-networks.github.io/api_docs/tns_10x/v1.0.0/" target="_blank">API routes</a></td>
<td>n/a </td>
<td>API support is limited to the following routes:  /login, /update, /poe_reset, /reboot, & /stats, and configuration is not supported.</td>
</tr>

<table>


