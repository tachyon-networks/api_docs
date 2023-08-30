

# Welcome to the Tachyon Networks API!

This repo contains the swagger-based docs for the Tachyon Networks Public API routes.  

### Usage & Examples

* Usage tips and details on the <a href="https://tachyon-networks.freshdesk.com/support/solutions/articles/67000659777-tna-30x-restful-api">Tachyon Support Site</a>
* Some <a href="https://github.com/tachyon-networks/api_docs/tree/master/_examples">example python scripts</a> (such as bulk firmware upgrade) can be found in this repo in the "_examples" folder.

<br/>

## API Specs

<table>
<tr> <td colspan="6"> <br/> <img width="25px" src="https://tachyon-networks.com/img/TNA30x-small.png""/> 
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


