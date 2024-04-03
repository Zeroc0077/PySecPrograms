import psutil
from datetime import datetime
import argparse

content = ""


def get_cpu_info():
    global content
    cpu_count = psutil.cpu_count()
    cpu_times = psutil.cpu_times_percent(interval=1)
    user_time = cpu_times.user
    system_time = cpu_times.system
    idle_time = cpu_times.idle
    content += "========================CPU INFO========================\n"
    content += f"[*]CPU Count(逻辑CPU个数):              {cpu_count}\n"
    content += f"[+]User Time(用户进程百分比):            {user_time}%\n"
    content += f"[+]System Time(系统进程百分比):          {system_time}%\n"
    content += f"[+]Idle Time(空闲时间百分比):            {idle_time}%\n"
    content += "========================================================\n\n"


def get_mem_info(unit="bytes"):
    global content
    mem = psutil.virtual_memory()
    total_mem = mem.total
    available_mem = mem.available
    used_mem = mem.used
    free_mem = mem.free
    swap_used = psutil.swap_memory().used
    if unit == "bytes":
        pass
    elif unit == "KB":
        total_mem = total_mem / 1024
        available_mem = available_mem / 1024
        used_mem = used_mem / 1024
        free_mem = free_mem / 1024
        swap_used = swap_used / 1024
    elif unit == "MB":
        total_mem = total_mem / 1024 / 1024
        available_mem = available_mem / 1024 / 1024
        used_mem = used_mem / 1024 / 1024
        free_mem = free_mem / 1024 / 1024
        swap_used = swap_used / 1024 / 1024
    elif unit == "GB":
        total_mem = total_mem / 1024 / 1024 / 1024
        available_mem = available_mem / 1024 / 1024 / 1024
        used_mem = used_mem / 1024 / 1024 / 1024
        free_mem = free_mem / 1024 / 1024 / 1024
        swap_used = swap_used / 1024 / 1024 / 1024
    content += "========================MEM INFO========================\n"
    content += f"[*]Total Memory(总内存):               %.2f {unit}\n" % total_mem
    content += f"[+]Available Memory(可用内存):         %.2f {unit}\n" % available_mem
    content += f"[+]Used Memory(已用内存):              %.2f {unit}\n" % used_mem
    content += f"[+]Free Memory(空闲内存):              %.2f {unit}\n" % free_mem
    content += f"[+]Swap Used(交换内存已用):             %.2f {unit}\n" % swap_used
    content += "========================================================\n\n"


def get_disk_info(unit="bytes"):
    global content
    disk = psutil.disk_io_counters()
    disk_read_count = disk.read_count
    disk_write_count = disk.write_count
    disk_read_bytes = disk.read_bytes
    disk_write_bytes = disk.write_bytes
    disk_read_time = disk.read_time
    disk_write_time = disk.write_time
    if unit == "bytes":
        pass
    elif unit == "KB":
        disk_read_bytes = disk_read_bytes / 1024
        disk_write_bytes = disk_write_bytes / 1024
    elif unit == "MB":
        disk_read_bytes = disk_read_bytes / 1024 / 1024
        disk_write_bytes = disk_write_bytes / 1024 / 1024
    elif unit == "GB":
        disk_read_bytes = disk_read_bytes / 1024 / 1024 / 1024
        disk_write_bytes = disk_write_bytes / 1024 / 1024 / 1024
    content += "========================DISK INFO=======================\n"
    content += f"[+]Disk Read Count(磁盘读取次数):       {disk_read_count}\n"
    content += f"[+]Disk Write Count(磁盘写入次数):      {disk_write_count}\n"
    content += f"[+]Disk Read Bytes(磁盘读取字节数):     %.2f {unit}\n" % disk_read_bytes
    content += f"[+]Disk Write Bytes(磁盘写入字节数):    %.2f {unit}\n" % disk_write_bytes
    content += f"[+]Disk Read Time(磁盘读取时间):        {disk_read_time}\n"
    content += f"[+]Disk Write Time(磁盘写入时间):       {disk_write_time}\n"
    content += "========================================================\n\n"


def get_net_info(unit="bytes"):
    global content
    net = psutil.net_io_counters()
    net_bytes_sent = net.bytes_sent
    net_bytes_recv = net.bytes_recv
    net_packets_sent = net.packets_sent
    net_packets_recv = net.packets_recv
    net_errin = net.errin
    net_errout = net.errout
    net_dropin = net.dropin
    net_dropout = net.dropout
    if unit == "bytes":
        pass
    elif unit == "KB":
        net_bytes_sent = net_bytes_sent / 1024
        net_bytes_recv = net_bytes_recv / 1024
    elif unit == "MB":
        net_bytes_sent = net_bytes_sent / 1024 / 1024
        net_bytes_recv = net_bytes_recv / 1024 / 1024
    elif unit == "GB":
        net_bytes_sent = net_bytes_sent / 1024 / 1024 / 1024
        net_bytes_recv = net_bytes_recv / 1024 / 1024 / 1024
    content += "========================NET INFO========================\n"
    content += f"[+]Net Bytes Sent(发送字节数):          %.2f {unit}\n" % net_bytes_sent
    content += f"[+]Net Bytes Recv(接收字节数):          %.2f {unit}\n" % net_bytes_recv
    content += f"[+]Net Packets Sent(发送数据包数):      {net_packets_sent}\n"
    content += f"[+]Net Packets Recv(接收数据包数):      {net_packets_recv}\n"
    content += f"[+]Net Errin(接收错误数):               {net_errin}\n"
    content += f"[+]Net Errout(发送错误数):              {net_errout}\n"
    content += f"[+]Net Dropin(接收丢包数):              {net_dropin}\n"
    content += f"[+]Net Dropout(发送丢包数):             {net_dropout}\n"
    content += "========================================================\n\n"


def get_user_info():
    global content
    current_user = psutil.users()[0]
    username = current_user.name
    start_time = datetime.fromtimestamp(
        current_user.started).strftime("%Y-%m-%d %H:%M:%S")
    PID = current_user.pid
    content += "========================USER INFO=======================\n"
    content += f"[*]Username(用户名):                  {username}\n"
    content += f"[+]Start Time(登录时间):              {start_time}\n"
    content += f"[+]PID(进程ID):                       {PID}\n"
    content += "========================================================\n"


argparser = argparse.ArgumentParser()
argparser.add_argument("-u", "--unit", help="unit of info, default is bytes")
argparser.add_argument("-o", "--output", help="output file")
args = argparser.parse_args()
unit = args.unit
output = args.output
if unit == None:
    unit = "GB"
if output == None:
    output = "host_info.txt"
output_file = open(output, "wb")

get_cpu_info()
get_mem_info(unit)
get_disk_info(unit)
get_net_info(unit)
get_user_info()
output_file.write(content.encode())
print(f"[*] Host Monitor Done! Output file: {output}")
