#include "sortvisualizer.h"
#include<iostream>

SortVisualizer::SortVisualizer(QWidget *parent1,int value1,QString img1):QFrame(parent1),value(value1),img(img1),parent(parent1) {
    if(img!="")
    {
        this->setStyleSheet(img);
    }
    this->setFrameShape(QFrame::Box);
    if(value>=0)
    {
        /**
         * @brief height
         * 将数字和高度成比例
         */
        int height=(double)value/100.0*300+30;
        this->setFixedSize(50,height);
    }
    else
    {
      //  this->setFixedHeight(400);
    }
}

void SortVisualizer::update()
{
    QFrame::update();
    if(value>0)
    {
        int height=(double)value/100.0*300+30;
        this->setFixedSize(50,height);
    }
    else
    {
        this->setFixedHeight(400);
    }

}


void SortVisualizer::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setPen(Qt::black);
    QRect rect(0,0,width(), height());
    QFont font("Arial", 14);
    painter.setFont(font);
    // 在矩形中绘制文本
    if(value>0) painter.drawText(rect, Qt::AlignCenter, numToStr(value));
    else if(value==-1) painter.drawText(rect, Qt::AlignCenter, "→");
    else if(value==-2) painter.drawText(rect, Qt::AlignCenter, "←");
    else if(value==-3) painter.drawText(rect, Qt::AlignCenter, "↑");
}

QString SortVisualizer::numToStr(int num)
{
    QString s="";
    QStack<int>* stack=new QStack<int>();
    while(num!=0)
    {
        stack->push(num%10);
        num=num/10;
    }
    while(!stack->empty())
    {
        s=s+(QChar)(stack->top()+'0');
        stack->pop();
    }
    delete stack;
    return s;
}

QPoint SortVisualizer::getPoint()
{
    return mapTo(parent,QPoint(0,0));
}

QSequentialAnimationGroup* SortVisualizer::moveOnly(SortVisualizer* frame)
{
    // 复制 QFrame
    SortVisualizer *copiedFrame = new SortVisualizer(parent,value,"");
    copiedFrame->setFrameShape(QFrame::Box);
    copiedFrame->setStyleSheet(img);
    copiedFrame->setFixedSize(this->size());
    QPoint p=this->mapTo(parent,QPoint(0,0));
    copiedFrame->move(p);
    copiedFrame->show();

    // 创建动画
    QPoint point=frame->getPoint();
    QPropertyAnimation *animation = new QPropertyAnimation(copiedFrame, "pos");
    animation->setDuration(500);
    animation->setStartValue(p);
    animation->setEndValue(QPoint(p.x(),p.y()-30)); // 指定目标位置

    //QPoint p1=frame->mapTo(parent,QPoint(0,0));
    QPropertyAnimation *animation1 = new QPropertyAnimation(copiedFrame, "pos");
    animation1->setDuration(2000);
    animation1->setStartValue(QPoint(p.x(),p.y()-30));
    animation1->setEndValue(QPoint(point.x(),p.y()-30));

    QPropertyAnimation *animation2 = new QPropertyAnimation(copiedFrame, "pos");
    animation2->setDuration(500);
    animation2->setStartValue(QPoint(point.x(),p.y()-30));
    animation2->setEndValue(QPoint(point.x(),p.y()));
    groupseq=new QSequentialAnimationGroup(copiedFrame);
    groupseq->addAnimation(animation);
    groupseq->addAnimation(animation1);
    groupseq->addAnimation(animation2);
    QObject::connect(groupseq, &QSequentialAnimationGroup::finished, [=]() {
        //copiedFrame->hide();
        copiedFrame->deleteLater();
        //update();
        //emit tableTotabel();
        //delete group;
    });
    return groupseq;
}

void SortVisualizer::moveFrameTo(SortVisualizer* frame)
{
    // 复制 QFrame
        SortVisualizer *copiedFrame = new SortVisualizer(parent,value,"");
        copiedFrame->setFrameShape(QFrame::Box);
        QString s=img;
        copiedFrame->setStyleSheet(s);
        copiedFrame->setFixedSize(this->size());
        QPoint p=this->mapTo(parent,QPoint(0,0));
        copiedFrame->move(p);
        copiedFrame->show();
        int temp=value;
        this->setValue(0);
        this->setStyleSheet("background-color: rgb(240,240);"
                            "border: none;");
        update();

        // 创建动画
        QPropertyAnimation *animation = new QPropertyAnimation(copiedFrame, "pos");
        animation->setDuration(500);
        animation->setStartValue(p);
        animation->setEndValue(QPoint(p.x(),p.y()-value)); // 指定目标位置

        QPoint p1=frame->mapTo(parent,QPoint(0,0));
        QPropertyAnimation *animation1 = new QPropertyAnimation(copiedFrame, "pos");
        animation1->setDuration(2000);
        animation1->setStartValue(QPoint(p.x(),p.y()-value));
        animation1->setEndValue(QPoint(p1.x(),p.y()-value));

        QPropertyAnimation *animation2 = new QPropertyAnimation(copiedFrame, "pos");
        animation2->setDuration(1000);
        animation2->setStartValue(QPoint(p1.x(),p.y()-value));
        animation2->setEndValue(QPoint(p1.x(),p.y()));

        QSequentialAnimationGroup *group=new QSequentialAnimationGroup(copiedFrame);
        group->addAnimation(animation);
        group->addAnimation(animation1);
        group->addAnimation(animation2);
        // 动画结束后销毁复制的 QFrame
        //QObject::connect(group, &QSequentialAnimationGroup::finished, copiedFrame,&SortVisualizer::deleteLater);
        QObject::connect(group, &QSequentialAnimationGroup::finished, [=]() {
            //copiedFrame->hide();
            copiedFrame->deleteLater();
            frame->setValue(temp);
            QString s=img;
            frame->setStyleSheet(s);
            frame->update();
            emit tableTotabel();
            //delete group;
        });
        group->start();
}

void SortVisualizer::exchange(SortVisualizer* frame)
{
    QSequentialAnimationGroup* seq_1=moveOnly(frame);
    QSequentialAnimationGroup* seq_2=frame->moveOnly(this);

    int temp1=value;
    int temp2=frame->getValue();
    setStyleSheet("background-color: rgb(240,240);"
                  "border: none;");
    frame->setStyleSheet("background-color: rgb(240,240);"
                         "border: none;");
    value=0;
    update();
    frame->setValue(0);
    frame->update();
    QParallelAnimationGroup * parallelGroup=new QParallelAnimationGroup;
    parallelGroup->addAnimation(seq_1);
    parallelGroup->addAnimation(seq_2);
    parallelGroup->start();
    QObject::connect(parallelGroup, &QParallelAnimationGroup::finished, [=]() {
        value=temp2;
        QString s=img;
        img=frame->getImg();
        frame->setImg(s);
        setStyleSheet(img);
        frame->setStyleSheet(frame->getImg());
        frame->setValue(temp1);
        update();
        frame->update();
        emit tableTotabel();
    });
}

int SortVisualizer::getValue()
{
    return value;
}

void SortVisualizer::setValue(int value1)
{
    value=value1;
}

QString SortVisualizer::getImg()
{
    return img;
}

void SortVisualizer::setImg(QString img1)
{
    img=img1;
}
