# tChat
tChat is a simple text chat with client and server apps

<h1> How to use ?</h1>

<p>
First of all, download tChat using git and <b>install watchdog python module</b> using pip. <br/>
Then, open server.py and change <b>ip</b> and <b>port</b> at this line : <i>serv_sock.bind(('127.0.0.1', 8000))</i> <br/>
Also, you should change <b>ip</b> and <b>port</b> in client.py at line : <i>client_sock.connect(('127.0.0.1', 8000))</i> <br/>
Then, change your name in config.json.
<hr>
After that you can run your server and client. <br/>
Open chat.txt with any text editor (BUT ! You should setup your editor in order to update your file, without closing editor)
<hr>
So, the best way is to use Atom or Sublime (They are already setupped)
</p>
