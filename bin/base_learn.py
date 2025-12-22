# 学E西安基础学习模块

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 自定义异常，用于跳过当前课程
class SkipToNextCourse(Exception):
    pass

def base_learn(driver, selector_index=1):
    """
    基础学习函数，支持动态选择器
    
    Args:
        driver: WebDriver实例
        selector_index: 选择器索引，用于选择第几个"进入学习"按钮
    """
    driver.implicitly_wait(5)  # 设置隐式等待
    mytime = 50  # 最大学习课程数
    
    # 根据选择器索引设置XPath选择器
    enter_learn_xpath = f"(//*[contains(text(), '进入学习')])[{selector_index}]"

    for sum in range(0, mytime):
        try:
            # 点击页面顶部的学习课堂按钮
            try:
                classroom = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='学习课堂']"))
                )
                classroom.click()
            except:
                print("未找到课程。请检查是否已打开学习网站并登录。")
                exit(1)
            print(f"\n第{sum+1}课学习")
            time.sleep(3)
            
            # 点击进入学习按钮
            try:
                btn2 = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, enter_learn_xpath))
                )
                btn2.click()
                time.sleep(3)
            except:
                print(f"无可学")
                break

            # 点击课程的开始学习/继续学习按钮
            try:
                all_windows_before = driver.window_handles
                try:
                    btn2 = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '继续学习')]"))
                )
                except:
                    btn2 = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '开始学习')]"))
                )
                btn2.click()
                time.sleep(3)
            except:
                print("已学完")
                break
                
            # 等待新窗口出现并切换
            WebDriverWait(driver, 10).until(
                lambda d: len(d.window_handles) > len(all_windows_before)
            )
            new_window = [w for w in driver.window_handles if w not in all_windows_before][0]
            driver.switch_to.window(new_window)
            
            # 关闭其他窗口逻辑
            current_window = driver.current_window_handle
            for handle in driver.window_handles:
                if handle != current_window:
                    driver.switch_to.window(handle)
                    driver.close()
            driver.switch_to.window(current_window)  # 切换回新窗口
            time.sleep(3)
            
            # 获取当前主窗口句柄
            main_window = driver.current_window_handle
            # 获取子课程列表
            classes = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "name"))
            )
            
            # 遍历学习每个子课程
            for index, element in enumerate(classes):
                print(f"\n开始学习第 {index+1} 个子课程: {element.text}")
                # 点击课程元素
                all_windows_before_sub = driver.window_handles
                element.click()
                time.sleep(2)  # 等待新标签页打开
                
                # 等待新窗口出现并切换
                WebDriverWait(driver, 20).until(
                    lambda d: len(d.window_handles) > len(all_windows_before_sub)
                )
                new_sub_window = [w for w in driver.window_handles if w not in all_windows_before_sub][0]
                driver.switch_to.window(new_sub_window)
                
                # 在新标签页等待
                error_count = 0  # 错误计数器
                str0 = "200"  # 错误指标
                while True:
                    try:
                        try:
                            vvstr_elements = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, "col-main"))
                            )
                            if vvstr_elements:
                                str1 = vvstr_elements[3].text
                                if str0 != str1:
                                    error_count = 0
                                    str0 = str1
                                else:
                                    error_count += 1  # 状态未改变时增加计数
                                print(".",end="",flush=True)
                        except:
                            error_count += 1  # 找不到元素时也增加计数
                            
                        if str1 == "100%":
                            driver.close()  # 关闭新标签页
                            driver.switch_to.window(main_window)  # 切换回主窗口
                            break  # 继续下一个子课程
                            
                        # 异常处理
                        if error_count >= 15:
                            print(f"\n检测到异常状态，尝试恢复流程")
                            current_window = driver.current_window_handle
                            all_windows = driver.window_handles
                            for window in all_windows:
                                if window != current_window:
                                    driver.switch_to.window(window)
                                    driver.close()
                            driver.switch_to.window(current_window)
                            driver.refresh()
                            time.sleep(5)
                            raise SkipToNextCourse()
                        time.sleep(10)
                    except SkipToNextCourse as e:
                        raise  # 重新抛出给外层
                    except Exception as e:
                        print(f"发生错误: {e}")
                        break
                time.sleep(5)

        except SkipToNextCourse:
            continue  # 直接进入下一个循环

        # 关闭所有非活动标签页
        current_window = driver.current_window_handle
        all_windows = driver.window_handles
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(current_window)  # 切换回活动标签页

def run_learn(driver, selector_index=1):
    """运行学习功能"""
    base_learn(driver, selector_index)