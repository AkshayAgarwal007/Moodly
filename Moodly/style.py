
qss='''

#Window1 {
background-color: rgb(255, 250, 175);
}

#Window2 {
background-color:#fff;
}

#pbar:horizontal {
    border: 1px solid gray;
    border-radius: 3px;
    background: white;
    padding: 1px;
    color:#000;
    text-align:center;
    font-family:Raleway;
}

#pbar::chunk:horizontal {
    background:  #33C3F0;
    color:#000;
    width: 25px;
    text-align:center;
}

#slbl {
    font-size: 15px;
    font-style:italic;
    color:red;
    font-family:Arial;
}

#nlbl {
    font-size: 15px;
    margin-left:80px;
    font-family:Raleway;
}

#ilbl {
    font-size: 15px;
    margin-left:65px;
    font-family:Raleway;
}

#hlbl {
    font-size: 15px;
    font-family:Raleway;
    color : #33C3F0 ;
    margin-left:5px;
}

#clbl {
    font-size: 15px;
    font-family:Raleway;
}

#lbl {
    font-size: 15px;
    font-family:Raleway;
}

#qle
{
    height: 20px;
    padding: 1px 1px;
    background-color: #fff;
    border: 1px solid #D1D1D1;
    border-radius: 4px;
}

#qle:focus {
    border: 1px solid #33C3F0;
    outline: 0;
}

#combo{
    height :20px;
}

#btn{
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:70px;
    background-color: #33C3F0;
    border-color: #33C3F0;
    font-family:Raleway;
}

#btn:hover {
    color: #FFF;
    background-color: #1EAEDB;
    border-color: #1EAEDB;
}

#gbtn {
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:50px;
    background-color: #07cc00;
    border-color: #07cc00;
    font-family:Raleway;
    margin-right:10px;
}

#gbtn:hover {
    color: #FFF;
    background-color: #06b200;
    border-color: #06b200;
}

#linkBtn {
    height: 38px;
    padding: 0 25px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:5px;
    background-color: #f7f7f7;
    border-color: #8f8f8f;
    font-family:Raleway;
    margin-right:10px;
}

#linkBtn:hover {
    color: #FFF;
    background-color: #dedede;
    border-color: #8f8f8f;
}

#obtn {
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:30px;
    background-color: #ED5F6F;
    border-color: #ED5F6F;
    font-family:Raleway;
    margin-right:10px;
}

#obtn:hover {
    color: #FFF;
    background-color: #e83146;
    border-color:#e83146;
}

#rbtn {
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:30px;
    background-color:#ff8f66;
    border-color:#ff8f66;
    font-family:Raleway;
    margin-right:10px;
}

#rbtn:hover {
    color: #FFF;
    background-color:#ff6a32;
    border-color: #ff6a32;
}

#sbtn {
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:30px;
    background-color: #33C3F0;
    border-color: #33C3F0;
    font-family:Raleway;
    margin-right:10px;
}

#sbtn:hover {
    color: #FFF;
    background-color: #1EAEDB;
    border-color: #1EAEDB;
}

#backBtn {
    height: 38px;
    padding: 0 30px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;
    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border-radius: 4px;
    border: 1px solid #bbb;
    color: #FFF;
    max-height:30px;
    max-width:60px;
    background-color: #33C3F0;
    border-color: #33C3F0;
    font-family:Raleway;
    margin-right:10px;
}

#backBtn:hover {
    color: #FFF;
    background-color: #1EAEDB;
    border-color: #1EAEDB;
}

#cFrameEven {
background-color: rgb(255, 250, 175);
min-height:140px;
min-width:806px;
}

#cFrameOdd {
background-color: rgb(255, 250, 175);
/*background-color:#F3F1EC;*/
min-height:140px;
min-width:806px;
}

QTabWidget::pane {
    border-top: 0px;
}

QTabWidget::tab-bar {
    left: 0px;
}

QTabBar::tab {
  font-weight:450;
  border-top-right-radius:15px;
  min-width:7em;
  padding: 12px;
  font-family:Raleway;
}

QTabBar::tab:selected, QTabBar::tab:hover {
   background-color: rgb(255, 250, 175);
}

QScrollArea {
  border:0px;
}

#nFrameEven {
background-color: rgb(255, 250, 175);
min-height:110px;
max-height:110px;
min-width:805px;
}

#nFrameOdd {
/*background-color: rgb(255, 250, 175);*/
background-color:#F5F5DC;
min-height:110px;
max-height:110px;
min-width:805px;
}

#nFrameDummy {
/*background-color: rgb(255, 250, 175);*/
background-color:#F5F5DC;
min-height:110px;
max-height:500px;
min-width:805px;
}


QStatusBar::item {
    border: 0px;
}

'''
