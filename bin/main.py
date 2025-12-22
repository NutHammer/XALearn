import chromedriver
import base_learn

def run_selected_script():
    print("————学E西安刷课工具————")
    web_address = "https://xian.sqgj.gov.cn/"
    driver = chromedriver.auto_chrome(web_address)
    while True:
        # 显示菜单选项
        print("="*25)
        print("输入 0 完成网络自学")
        print("输入 整数n 完成第n个专题学习") 
        print("输入 A 学习全部课程")
        print("输入 Q 退出程序")
        
        # 选择功能
        choice = input("请输入：")
        
        if choice.lower() == 'q':
            print("程序退出")
            break
        elif choice.lower() == 'a':
            print("开始学习所有课程...")
            for i in range(10):
                try:
                    print(f"\n正在学习专题 {i}...")
                    base_learn.base_learn(driver,i + 1)
                except Exception as e:
                    print(f"\n专题 {i} 已学完或发生错误")
                    print("继续执行下一个专题...")
        else:
            try:
                choice = int(choice)
                if 0 <= choice <= 9:
                    base_learn.base_learn(driver,choice + 1)
            except ValueError:
                print("请输入有效的整数（0-9）或A（执行所有选项）")

if __name__ == "__main__":
    run_selected_script()