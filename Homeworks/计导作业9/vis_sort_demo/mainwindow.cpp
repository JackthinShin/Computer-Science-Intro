#include "mainwindow.h"
#include "ui_mainwindow.h"
#include<iostream>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    z_frame1=new SortVisualizer(this,10,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame2=new SortVisualizer(this,30,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame3=new SortVisualizer(this,73,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame4=new SortVisualizer(this,24,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame5=new SortVisualizer(this,12,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame6=new SortVisualizer(this,1,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame7=new SortVisualizer(this,45,"QFrame{background-color: rgb(173, 216, 230);}");
    z_frame8=new SortVisualizer(this,57,"QFrame{background-color: rgb(173, 216, 230);}");

    ui->horizontalLayout->addWidget(z_frame1,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame2,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame3,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame4,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame5,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame6,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame7,0,Qt::AlignBottom);
    ui->horizontalLayout->addWidget(z_frame8,0,Qt::AlignBottom);

    connect(ui->pushButton,&QPushButton::clicked,this,&MainWindow::action);
    connect(z_frame1,&SortVisualizer::tableTotabel,this,&MainWindow::actionEnd);

}

void MainWindow::actionEnd()
{
    //动画结束
}

void MainWindow::action()
{
    /**
     * 算法逻辑
     */
    frameAction(z_frame8,z_frame5,1);//1:frame互相交换,2:frame1移动到frame2
  //  frameAction(z_frame2,z_frame1,1);//1:frame互相交换,2:frame1移动到frame2
}

void MainWindow::frameAction(SortVisualizer* frame1,SortVisualizer* frame2,int tag)
{
    if(tag==1)
    {
        frame1->exchange(frame2);
    }
    else if(tag==2)
    {
        frame1->moveFrameTo(frame2);
    }

}

MainWindow::~MainWindow()
{
    delete ui;
}
