#include "widget.h"
#include "./ui_widget.h"
#include "personmodel.h"
#include <QInputDialog>
#include <QMessageBox>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);

    model = new PersonModel(this);

    ui->listView->setModel(model);
    ui->tableView->setModel(model);
    ui->treeView->setModel(model);

    ui->tableView->setSelectionModel(ui->listView->selectionModel());
    ui->treeView->setSelectionModel(ui->listView->selectionModel());
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_add_person_button_clicked()
{
    bool ok;
    QString name = QInputDialog::getText(nullptr, "Names",
                                         tr("Person name:"), QLineEdit::Normal,
                                         "Type in name", &ok);

    if( ok && !name.isEmpty()){

        int age = QInputDialog::getInt(nullptr,"Person Age","Age",20,15,120);

        Person* person = new Person(name, "blue", age, this);
        model->addPerson(person);

    }else{
        QMessageBox::information(nullptr,"Failure","Must specify name and age");
    }
}


void Widget::on_remove_person_button_clicked()
{

    QModelIndex index = ui->listView->currentIndex();
    model->removePerson(index);

}

