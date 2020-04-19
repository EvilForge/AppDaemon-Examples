# Notes:

AppDaemon was installed in my case using a hassio plugin (automated) install, where you get it from the store and install it
easily. Your install may be different, so read the docs! 

I didnt see anything easy to tell me where it all was, or how to get to the console, or anything.
I know its all in the docs, right? I just couldnt find it immediately. So heres some tidbits:

1. After appdaemon starts, you will have a new console at http://hassio-server-ip:5050
2. The entities page on the appdaemon console is really handy. But you still need to restart HA and 
    remove old entities if you want to see them drop from this view.
3. The Appdaemon page really wants my entire 4k TV screen to show all fields completely, despite there being spare screen space. But
    you can still doubleclick on a field to select the entire value. (handy for writing scripts)
4. Constraints!  Love them! Then I hated them! For some of my code, like AC controls, I only wanted to set a temperature for a period of 
    time each day. A constraint is NOT the way to block AC activity outside that time. Because my script uses a 'run_in" callback 
    timer, and then sets the next callback in the code. A constraint blocks that callback 'reset' outside the allowed times. This means
    that your script will run during the constraint period, then never ever again after the period ends, because it will never be able 
    to set a callback outside your allowed period.  The same situation occurs with a boolean constraint. So take that in mind.. 
5. Calling a funciton you defined in your own class and Python says it can't find it? You might need to put "self." in front of the
    function name or Python might not be able to find it.
6. If youre still having issues figuring out how arguments are passed, and how you access them in your script to do things or use them... 
    you are not alone!  But you will start to "get it" if you play with the scripts long enough.
7. The AppDaemon API docs are REALLY helpful for me. https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html
8. Using VSCode or a more intelligent python editor IDE will help you. Don't rely on the built in file configurator in hassio for most of
    your coding. It works fine but.. VSCode sure works better, IMHO.

