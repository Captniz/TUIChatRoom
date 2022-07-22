# TUI Chat room (still have to give it a proper name) <!-- omit in toc -->

---

## 🔠 Index<!-- omit in toc -->

- [❓ What is it?](#-what-is-it)
- [🔀 How does it work?](#-how-does-it-work)
- [✔ How to use?](#-how-to-use)
- [🤝 Contribute](#-contribute)
- [🚗 Roadmap](#-roadmap)
- [💡 Resources](#-resources)
- [📃 Licensing](#-licensing)
- [🔄 Project status](#-project-status)

---

## ❓ What is it?

This is a WIP about a terminal application that provides a simple chat room. It was originally meant to share short messages in LAN without needing a internet connection

---

## 🔀 How does it work?

The main packages used in this program are `curses` and `socket`, both preinstalled if you have a linux machine.

**Curses** is responsible for the graphic interface and everything that is visible on the screen generally

**Socket** is responsible of the transmission of the messages between server and clients

---
## ✔ How to use?

First, download the `*Version*.zip` then follow this instructions:

**HOST A LAN SERVER:**

> Just open `Server.py` and a server will be opened on your local IP, it's that easy!



**CONNECT TO A LAN SERVER**

> Just open `Client.py` and follow the instructions on screen, it's that easy!  
> *(Watch out, it's important to keep the program window fullscreen or else it may crash)*

---

## 🤝 Contribute

Opening issues on github to point out the weak spots of the program it's extremely helpful to me, thanks in advance!

---

## 🚗 Roadmap

[x] Add a server history  
[ ] Add a message history    
[ ] Make it not only LAN but also accessible for the internet   
[ ] Put automatically the client window fullscreen   
[ ] Clear up the code  
[ ] Make it good to look at  

---

## 💡 Resources

**Tutorials:**  
- [Sockets](https://www.youtube.com/watch?v=3QiPPX-KeSc&t=1141s)
- [Curses](https://www.youtube.com/playlist?list=PLzMcBGfZo4-n2TONAOImWL4sgZsmyMBc8)
- [Curses_Documentation](https://docs.python.org/3/howto/curses.html)

**Packages/Cool things**
- [RichText](https://github.com/Textualize/rich)
- [Textualize](https://github.com/Textualize/textual)

**Isparation**
- [GupShup](https://www.reddit.com/r/unixporn/comments/u5ql0w/oc_gupshup_chat_in_the_terminal/)
- [r/Commandline](https://www.reddit.com/r/commandline/)

---  

## 📃 Licensing

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licenza Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Quest'opera è distribuita con Licenza <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribuzione - Non commerciale - Condividi allo stesso modo 4.0 Internazionale</a>.

---

## 🔄 Project status

WIP, but there are already a few (somewhat functioning) pre-release versions you can try