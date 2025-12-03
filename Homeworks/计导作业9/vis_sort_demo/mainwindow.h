#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include"sortvisualizer.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:
    void action();
    void actionEnd();
    void frameAction(SortVisualizer* frame1,SortVisualizer* frame2,int tag);

private:
    Ui::MainWindow *ui;

    SortVisualizer* z_frame1=nullptr;
    SortVisualizer* z_frame2=nullptr;
    SortVisualizer* z_frame3=nullptr;
    SortVisualizer* z_frame4=nullptr;
    SortVisualizer* z_frame5=nullptr;
    SortVisualizer* z_frame6=nullptr;
    SortVisualizer* z_frame7=nullptr;
    SortVisualizer* z_frame8=nullptr;
    SortVisualizer* z_frame9=nullptr;
    SortVisualizer* z_frame10=nullptr;


};
#endif // MAINWINDOW_H
