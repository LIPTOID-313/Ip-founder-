import os
import socket
import subprocess
from prettytable import PrettyTable

def clear_screen():
    """يمسح الشاشة."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_banner():
    """يطبع الشعار."""
    banner = """
    ________     __    ____  ________  ______ 
   /  _/ __ \\   / /   / __ \\/ ____/ / / / __ \\
   / // /_/ /  / /   / / / / /   / / / / /_/ /
 _/ // ____/  / /___/ /_/ / /___/ /_/ / ____/ 
/___/_/      /_____/\\____/\\____/\\____/_/      
                                              
    """
    print(banner)

def get_ip_address(hostname):
    """يحصل على عنوان IP من اسم النطاق."""
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving hostname: {e}")
        return None

def validate_hostname(hostname):
    """يتحقق من صحة اسم النطاق."""
    if not hostname:
        print("Hostname cannot be empty.")
        return False
    if hostname.count('.') < 1:
        print("Hostname seems invalid. Make sure it's a valid domain name.")
        return False
    return True

def ping_ip(ip_address):
    """ينفذ أمر ping لعنوان IP."""
    try:
        result = subprocess.run(['ping', ip_address, '-n', '1'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error executing ping command: {e}")
        return False

def scan_ip_range(ip_prefix):
    """يبحث في نطاق عناوين IP ويعرض النتائج في جدول."""
    table = PrettyTable()
    table.field_names = ["IP Address", "Status"]
    
    for i in range(1, 255):
        ip_address = f"{ip_prefix}.{i}"
        if ping_ip(ip_address):
            table.add_row([ip_address, "Reachable"])
        else:
            table.add_row([ip_address, "Not Reachable"])
    
    print(table)

def main():
    while True:
        clear_screen()
        draw_banner()
        
        # طلب رابط الموقع من المستخدم
        url = input("Enter the website URL or hostname (e.g., example.com): ").strip()
        
        # التحقق من صحة اسم النطاق
        if not validate_hostname(url):
            continue
        
        # استخراج عنوان IP من اسم النطاق
        ip_address = get_ip_address(url)
        
        if ip_address:
            print(f"IP Address of {url}: {ip_address}")
            
            # تحليل النطاق (أول 3 أجزاء من عنوان IP)
            ip_prefix = '.'.join(ip_address.split('.')[:3])
            
            print("Scanning IP range...")
            scan_ip_range(ip_prefix)
        else:
            print("Could not resolve IP address.")
        
        # طلب إدخال من المستخدم للعودة إلى القائمة الرئيسية
        input("Press any key to return to the main menu...")

if __name__ == '__main__':
    main()