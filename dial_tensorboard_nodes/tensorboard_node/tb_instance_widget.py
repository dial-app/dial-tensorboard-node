# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget


class TensorboardInstanceWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

    def sizeHint(self) -> "QSize":
        return QSize(200, 200)

TensorboardInstanceWidgetFactory = providers.Factory(TensorboardInstanceWidget)
