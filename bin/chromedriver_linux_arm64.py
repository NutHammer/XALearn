
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


def auto_chrome(web_address):
    # Firefox安装路径（当前文件向上一级目录下的res中）
    firefox_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "firefox")
    )
    
    # 确保Firefox可执行文件存在
    if not os.path.exists(firefox_path):
        raise FileNotFoundError(f"找不到Firefox浏览器，请确保Firefox存在于 {firefox_path}")
    
    # 创建持久化配置文件目录
    profile_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "profile")
    )
    # 本地geckodriver驱动路径
    driver_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "geckodriver")
    )
    
    if not os.path.exists(driver_path):
        raise FileNotFoundError("geckodriver驱动文件不存在")
    
    # 确保驱动文件有执行权限（Linux/macOS）
    if not os.access(driver_path, os.X_OK):
        os.chmod(driver_path, 0o755)
    
    # 创建Firefox选项
    firefox_options = Options()
    
    # 指定Firefox二进制文件路径
    firefox_options.binary_location = firefox_path
    
    # 使用持久化配置文件
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
       
    # 通过命令行参数指定配置文件路径
    firefox_options.add_argument(f'--profile={profile_path}')
    
    # 添加常用选项以提高兼容性
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-first-run')
    firefox_options.add_argument('--no-default-browser-check')

    # 设置自动播放偏好
    firefox_options.set_preference("media.autoplay.default", 0)  # 0 = 允许所有自动播放
    firefox_options.set_preference("media.autoplay.blocking_policy", 0)  # 0 = 不阻止自动播放
    firefox_options.set_preference("media.autoplay.block-event.enabled", False)  # 允许自动播放事件
    
    # 设置静音偏好
    firefox_options.set_preference("media.volume_scale", 0)  # 0 = 完全静音
    
    # 创建服务
    service = Service(executable_path=driver_path)
    
    # 创建驱动实例
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # 打开指定网址
    driver.get(web_address)
    
    return driver

