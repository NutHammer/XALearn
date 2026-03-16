# 学E西安基础学习模块

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 自定义异常，用于跳过当前课程
class SkipToNextCourse(Exception):
    pass

class BaseLearn:
    """
    基础学习类，支持动态选择器和UI处理
    """
    def __init__(self, driver, ui_handler=None):
        """
        初始化BaseLearn类
        
        Args:
            driver: WebDriver实例
            ui_handler: UI处理实例，用于显示信息
        """
        self.driver = driver
        self.ui_handler = ui_handler
        self.driver.implicitly_wait(5)  # 设置隐式等待
        self.mytime = 50  # 最大学习课程数
    
    def _print(self, message):
        """
        打印消息，优先使用UI处理实例
        
        Args:
            message: 要打印的消息
        """
        if self.ui_handler:
            self.ui_handler.print_to_window(message)
        else:
            print(message)
    
    def run_learning_cycle(self, button_index=1):
        """
        运行学习循环
        
        Args:
            button_index: 选择器索引，用于选择第几个"进入学习"按钮
        """
        # 根据选择器索引设置XPath选择器
        enter_learn_xpath = f"(//*[contains(text(), '进入学习')])[{button_index}]"

        for sum in range(0, self.mytime):
            try:
                # 点击页面顶部的学习课堂按钮
                try:
                    classroom = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='学习课堂']"))
                    )
                    classroom.click()
                except:
                    self._print("未找到课程。请检查是否已打开学习网站并登录。")
                    break
                time.sleep(3)
                
                # 点击进入学习按钮
                try:
                    btn2 = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, enter_learn_xpath))
                    )
                    btn2.click()
                    time.sleep(3)
                except:
                    self._print(f"专题不存在")
                    break

                # 点击课程的开始学习/继续学习按钮
                all_windows_before = self.driver.window_handles
                try:
                    try:
                        btn2 = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '继续学习')]"))
                    )
                    except:
                        btn2 = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '开始学习')]"))
                    )
                    btn2.click()
                    time.sleep(3)
                except:
                    self._print("已学完")
                    break
                    
                # 等待新窗口出现并切换
                try:
                    WebDriverWait(self.driver, 10).until(
                        lambda d: len(d.window_handles) > len(all_windows_before)
                    )
                    new_windows = [w for w in self.driver.window_handles if w not in all_windows_before]
                    if new_windows:
                        new_window = new_windows[0]
                        self.driver.switch_to.window(new_window)
                    else:
                        self._print("已学完")
                        break
                except:
                    self._print("已学完")
                    break
                
                # 检查并初始化悬浮窗
                if self.ui_handler:
                    self.ui_handler._check_floating_window()
                
                # 关闭其他窗口逻辑
                current_window = self.driver.current_window_handle
                for handle in self.driver.window_handles:
                    if handle != current_window:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                self.driver.switch_to.window(current_window)  # 切换回新窗口
                
                # 检查并初始化悬浮窗
                if self.ui_handler:
                    self.ui_handler._check_floating_window()
                
                time.sleep(3)
                
                # 获取当前主窗口句柄
                main_window = self.driver.current_window_handle
                # 获取子课程列表
                self._print(f"第{sum+1}课学习")
                try:
                    classes = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
                    )
                except:
                    self._print("已学完")
                    break
                
                # 遍历学习每个子课程
                for index, element in enumerate(classes):
                    self._print(f"\n开始学习第 {index+1} 个子课程: {element.text}\n若出现异常，程序将在4分钟后重试。")
                    # 点击课程元素
                    all_windows_before_sub = self.driver.window_handles
                    element.click()
                    time.sleep(2)  # 等待新标签页打开
                    
                    # 等待新窗口出现并切换
                    try:
                        WebDriverWait(self.driver, 20).until(
                            lambda d: len(d.window_handles) > len(all_windows_before_sub)
                        )
                        new_sub_windows = [w for w in self.driver.window_handles if w not in all_windows_before_sub]
                        if new_sub_windows:
                            new_sub_window = new_sub_windows[0]
                            self.driver.switch_to.window(new_sub_window)
                        else:
                            self._print("已学完")
                            break
                    except:
                        self._print("已学完")
                        break
                    
                    # 检查并初始化悬浮窗
                    if self.ui_handler:
                        self.ui_handler._check_floating_window()
                    
                    # 在新标签页等待
                    error_count = 0  # 错误计数器
                    str0 = "200"  # 错误指标
                    while True:
                        try:
                            vvstr_elements = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, "col-main"))
                            )
                            if vvstr_elements:
                                str1 = vvstr_elements[3].text
                                if str0 != str1:
                                    error_count = 0
                                    str0 = str1
                                else:
                                    error_count += 1  # 状态未改变时增加计数
                            # 移除打印进度点，因为UI可能会导致性能问题
                            # self._print(".", end="", flush=True)
                        except:
                            error_count += 1  # 找不到元素时也增加计数
                            
                        if str1 == "100%":
                            try:
                                self.driver.close()  # 关闭新标签页
                                self.driver.switch_to.window(main_window)  # 切换回主窗口
                                
                                # 检查并初始化悬浮窗
                                if self.ui_handler:
                                    self.ui_handler._check_floating_window()
                                
                                break  # 继续下一个子课程
                            except:
                                self._print("已学完")
                                break
                                
                        # 异常处理
                        if error_count >= 15:
                            self._print(f"\n检测到异常状态，尝试恢复流程")
                            try:
                                current_window = self.driver.current_window_handle
                                all_windows = self.driver.window_handles
                                for window in all_windows:
                                    if window != current_window:
                                        self.driver.switch_to.window(window)
                                        self.driver.close()
                                self.driver.switch_to.window(current_window)
                                self.driver.refresh()
                                time.sleep(5)
                            except:
                                self._print("已学完")
                                break
                            raise SkipToNextCourse()
                        time.sleep(10)
                    time.sleep(1)
            except SkipToNextCourse:
                continue  # 直接进入下一个循环


            # 关闭所有非活动标签页
            try:
                current_window = self.driver.current_window_handle
                all_windows = self.driver.window_handles
                for window in all_windows:
                    if window != current_window:
                        self.driver.switch_to.window(window)
                        self.driver.close()
                self.driver.switch_to.window(current_window)  # 切换回活动标签页
                
                # 检查并初始化悬浮窗
                if self.ui_handler:
                    self.ui_handler._check_floating_window()
            except:
                self._print("已学完")
                break

def run_learn(driver, selector_index=1):
    """运行学习功能"""
    # 兼容旧的API
    learner = BaseLearn(driver)
    learner.run_learning_cycle(button_index=selector_index)