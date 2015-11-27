
qss='''

#Window1
{
background-color: rgb(255, 250, 175);
}

#Window2
{
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
    margin-left:100px;
    font-family:Raleway;

}

#hlbl {

    font-size: 15px;
    font-family:Raleway;
    color : red ;

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
    outline: 0; }

#combo
{
    height: 20px;
    padding: 1px 1px;
    background-color: #fff;
    bord    er: 1px solid #D1D1D1;
    border-radius: 4px;



}

#combo:focus {
    border: 1px solid #33C3F0;
    outline: 0; }

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

#btn:hover
{
    color: #FFF;
    background-color: #1EAEDB;
    border-color: #1EAEDB;

}

#gbtn{

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

#gbtn:hover
{
    color: #FFF;
    background-color: #06b200;
    border-color: #06b200;

}

#linkBtn{

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
    background-color: #6666ff;
    border-color: #6666ff;
    font-family:Raleway;
    margin-right:10px;
}

#linkBtn:hover
{
    color: #FFF;
    background-color: #3232FF;
    border-color: #3232FF;

}

#obtn{

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
    background-color: #ED5F6F;
    border-color: #ED5F6F;
    font-family:Raleway;

    margin-right:10px;
}

#obtn:hover
{
    color: #FFF;
    background-color: #e83146;
    border-color: #e83146;

}
#sbtn{

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

#sbtn:hover
{
    color: #FFF;
    background-color: #1EAEDB;
    border-color: #1EAEDB;

}


#backBtn{

    height: 38px;
    padding: 0 20px;
    color: #555;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 38px;

    text-transform: uppercase;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;


    color: #FFF;
    max-height:30px;
    max-width:1px;
    background-color: rgb(255, 250, 175);
    font-family:Raleway;

}

#backBtn:hover
{
    color: #FFF;
    background-color: rgb(255, 250, 175);


}

#cFrameEven
{
background-color: rgb(255, 250, 175);
min-height:140px;
min-width:806px;
}


#cFrameOdd
{
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

 QScrollArea
 {
  border:0px;
 }



 #nFrameEven
{
background-color: rgb(255, 250, 175);
min-height:110px;
max-height:110px;
min-width:805px;
}


#nFrameOdd
{
/*background-color: rgb(255, 250, 175);*/
background-color:#F5F5DC;
min-height:110px;
max-height:110px;
min-width:805px;
}

#nFrameDummy
{
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
