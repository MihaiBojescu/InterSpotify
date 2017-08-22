#!/usr/bin/env python3
import sys
import signal
import socket
import requests
from selenium import webdriver
from html.parser import HTMLParser

class proxy(object):
    def __init__(self):
        object.__init__(self)
        self.IP = ""
        self.port = 0

class ProxyListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.record = False
        self.proxies = []
        self.currentProxy = {}

    def handle_starttag(self, tag, attributes):
        if tag == "td":
            self.record = True

    def handle_endtag(self, tag):
        if tag == "td":
            self.record = False

    def handle_data(self, data):
        if self.record:
            if self.isIP(data):
                self.currentProxy = proxy()
                self.currentProxy.IP = data

            elif self.isPort(data):
                self.currentProxy.port = int(data)
                self.proxies.append(self.currentProxy)

    def isPort(self, data):
        try:
            int(data)
            return True
        except ValueError:
            return False

    def isIP(self, data):
        try:
            values = data.split(".")

            for value in values:
                integer = int(value)
                if integer < 0 or integer >= 256:
                    return False

            return True
        except ValueError:
            return False

def updateProxyList():
    site = requests.get("https://us-proxy.org/")
    data = ProxyListParser()
    data.feed(site.text)
    data.close()
    print("Got " + str(len(data.proxies)) + " proxies from the USA.")
    return data.proxies

def loginToSpotify(proxies):
    for proxy in proxies:
        try:
            print("Trying proxy " + str(proxy.IP) + ":" + str(proxy.port) + ".")
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", proxy.IP)
            profile.set_preference("network.proxy.http_port", proxy.port)
            profile.set_preference("network.proxy.ssl", proxy.IP)
            profile.set_preference("network.proxy.ssl_port", proxy.port)
            profile.set_preference('network.proxy.socks', proxy.IP)
            profile.set_preference('network.proxy.socks_port', proxy.port)
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile=profile)
            driver.get("https://play.spotify.com/")
            signal.pause()

        except KeyboardInterrupt:
            print("Quitting.")
            sys.exit()

        except:
            answer = ""
            while answer != "y" and answer != "n":
                answer = input("Did it work? y/n: ")

            if answer == "y":
                print("Have a great day!")
                sys.exit()
            else:
                print("Next proxy")


if __name__ == "__main__":
    proxies = updateProxyList()
    loginToSpotify(proxies)
