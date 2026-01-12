import time
import random
import os
import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# Bilibili 动态批量删除脚本 (Edge浏览器版)
# ==========================================

def setup_driver():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    # 规避自动化检测
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    # 自动获取脚本所在目录
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        try:
            application_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            application_path = os.getcwd()

    # 驱动路径配置
    driver_path = os.path.join(application_path, "msedgedriver.exe")
    
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"驱动文件缺失: {driver_path}\n请确保 msedgedriver.exe 与脚本在同一目录下。")
    
    service = Service(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

def delete_bilibili_dynamics():
    driver = None
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        return

    try:
        print("正在打开 Bilibili 首页...")
        driver.get("https://www.bilibili.com/")
        print("👉 请在弹出的浏览器中完成扫码登录。")
        input("✅ 登录成功后，请在控制台按回车键 [Enter] 继续...")

        # 获取用户输入 UID
        uid = input("请输入您的 Bilibili UID (个人空间网址后的数字): ").strip()
        if not uid:
            print("UID 不能为空！")
            return

        target_url = f"https://space.bilibili.com/{uid}/dynamic"
        print(f"即将前往: {target_url}")
        driver.get(target_url)
        time.sleep(3) 

        deleted_count = 0
        
        # 元素定位路径配置 (根据 B 站前端结构更新)
        # 注意：如果 B 站更新网页结构，这里的 XPath 可能需要修改
        three_dots_xpath = "/html/body/div/main/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div/div[2]/div[3]/div/div"
        confirm_btn_xpath = "/html/body/div[2]/div[2]/div[4]/button[2]"

        # 连续失败计数器 (用于判断是否翻页到底)
        fail_count = 0 
        max_fail_attempts = 3

        while True:
            try:
                # --- 1. 尝试寻找“三个点”菜单按钮 ---
                try:
                    # 使用显式等待寻找元素
                    menu_btn = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, three_dots_xpath))
                    )
                    
                    # 找到按钮了，重置失败计数
                    fail_count = 0 
                    
                    # 滚动到可见区域
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_btn)
                    time.sleep(0.5)
                    
                    # 点击菜单
                    menu_btn.click()

                except:
                    # --- 未找到按钮：进入滚动加载逻辑 ---
                    fail_count += 1
                    print(f"⏳ 当前页面暂无内容，尝试向下滚动加载 ({fail_count}/{max_fail_attempts})...")
                    
                    # 滚动到底部
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3) # 等待网络加载
                    
                    # 往回滚一点再滚下去，触发部分懒加载机制
                    driver.execute_script("window.scrollBy(0, -300);")
                    time.sleep(0.5)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    if fail_count >= max_fail_attempts:
                        print("🎉 连续多次加载失败，判定所有动态已删除完毕。")
                        break
                    
                    continue # 重新循环检查

                # --- 2. 点击“删除”文字 ---
                time.sleep(0.5)
                try:
                    delete_text_option = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '删除')]"))
                    )
                    delete_text_option.click()
                except:
                    driver.execute_script("document.body.click();") # 点击空白处关闭菜单
                    continue

                # --- 3. 点击“确定”按钮 ---
                time.sleep(0.5)
                try:
                    confirm_btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, confirm_btn_xpath))
                    )
                    confirm_btn.click()
                except:
                    driver.execute_script("document.body.click();")
                    continue
                
                deleted_count += 1
                print(f"✅ 已删除第 {deleted_count} 条动态")
                
                # --- 4. 等待列表刷新 (防止操作过快报错) ---
                time.sleep(random.uniform(2.0, 3.0))

            except Exception as e:
                print(f"⚠️ 发生意外错误: {e}")
                time.sleep(2)
                continue

    except Exception as e:
        print(f"脚本出错: {e}")
    finally:
        print(f"任务结束，本次共删除 {deleted_count} 条。")

if __name__ == "__main__":
    delete_bilibili_dynamics()