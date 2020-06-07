
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
import shutil


class App:
    def __init__(self,username='',password='',
                 target_username='', path='C:\\Users\\Azeet\\Desktop\\instafoto'):
        self.username=username
        self.password=password
        self.target_username=target_username
        self.path=path
        self.driver=webdriver.Chrome('chromedriver')
        self.error=False
        self.main_url='https://www.instagram.com'
        self.driver.get(self.main_url)
        sleep(5)
        self.log_in()
        if self.error is False:
            self.close_dialog_box()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()
        sleep(5)
        self.driver.close()
            
            
    
    def downloading_images(self):
        soup=BeautifulSoup(self.driver.page_source,'lxml')
        all_images=soup.find_all('img')
        print('Length of all images',len(all_images))
        #for image in all_images:
            #print(image['src'])
        for index, image in enumerate(all_images):
            filename='image_'+str(index)+'.jpg'
            image_path=os.path.join(self.path,filename)
            link=image['src']
            print('Downloading image',index)
            response=requests.get(link,stream=True)
            try:
                with open(image_path,'wb') as file:
                    shutil.copyfileobj(response.raw,file) #(source,destination)
            except Exception as e:
                print(e)
                print('couldnot download image number',index)
                print('image link---->>',link)
        
        
            
    def scroll_down(self):
        try:
            no_of_posts=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span')
            no_of_posts=str(no_of_posts.text).replace(',','')
            no_of_posts=no_of_posts.replace(' posts','')
            self.no_of_posts=int(no_of_posts)
            print(self.no_of_posts)
            if self.no_of_posts>12:
                no_of_scrolls=int(self.no_of_posts/12)+3
                try:
                    for value in range(no_of_scrolls):
                        print(value)
                        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                        sleep(3)
                except Exception as e:
                    self.error=True
                    print(e)
                    print('some error occured during scrolling down')
            sleep(10)
        except Exception:
            self.error=True
            print('could not find the number of posts while scrolling down')
                    

        
    
    def open_target_profile(self):
        try:
            #search_bar=driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
            #search_bar.send_keys('netgeo')
            target_profile_url=self.main_url+'/'+self.target_username+'/'
            self.driver.get(target_profile_url)
            sleep(3)
        except Exception:
            self.error=True
            print('username incorrect maybe?')
    
    def close_settings_window_if_there(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception as e:
            pass
    
    def close_dialog_box(self):
        try:
            sleep(10)
            close_btn=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
            sleep(3)
            close_btn.click()
            sleep(5)
            close_btn1=self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
            sleep(3)
            close_btn1.click()
            sleep(1)
        except Exception:
            pass
            
            
            
            
    def log_in(self,):
        try:
            user_name_input=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
            user_name_input.send_keys(self.username)
            password_input=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
            password_input.send_keys(self.password)
            user_name_input.submit()
            #password_input.submit()
            self.close_settings_window_if_there()
        except Exception:
            self.error=True
            print('some error occured while trying to login')
        
if __name__=='__main__':
    app=App()	