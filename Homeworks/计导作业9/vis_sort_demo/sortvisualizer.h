#ifndef SORTVISUALIZER_H
#define SORTVISUALIZER_H

#include <QApplication>
#include <QWidget>
#include <QFrame>
#include<QSequentialAnimationGroup>
#include<QPropertyAnimation>
#include<QString>
#include<QPaintEvent>
#include<QPainter>
#include<QRect>
#include<QStack>
#include<QParallelAnimationGroup>

class SortVisualizer: public QFrame
{
    Q_OBJECT
signals:
    void tableTotabel();

public slots:
    void update();

public:
    SortVisualizer(QWidget *parent1 = nullptr,int value1=0,QString img1="");

    QSequentialAnimationGroup* moveOnly(SortVisualizer* frame); //得到frame的动画对象
    int getValue();
    void setValue(int vbalue1);
    QString getImg();
    void setImg(QString img1);
    void paintEvent(QPaintEvent *event);
    QString numToStr(int num);
    QPoint getPoint();

    void moveFrameTo(SortVisualizer* frame); //移动frame到另一个frame的位置
    void exchange(SortVisualizer* frame); //两个frame交换位置

private:
    int value=0;
    QString img;
    QWidget *parent=nullptr;
    QSequentialAnimationGroup *groupseq=nullptr;
};

#endif // SORTVISUALIZER_H
