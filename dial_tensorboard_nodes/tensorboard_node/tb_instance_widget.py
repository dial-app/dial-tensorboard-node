# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from typing import List
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tensorboard import program
from tensorflow.keras.callbacks import Callback

LOGGER = log.get_logger(__name__)


class TensorboardInstanceWidget(QWidget):
    tensorboard_status = "Stopped"
    tensorboard_url = ""

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._status_label = QLabel(self.tensorboard_status)
        self._url_label = QLabel(self.tensorboard_url)

        self._logs_path_textbox = QLineEdit()
        self._logs_path_textbox.setPlaceholderText("Directory to store log files...")
        self._logs_path_button = QPushButton("Select...")
        self._logs_path_button.clicked.connect(self._pick_logs_directory)

        self._logs_path_layout = QHBoxLayout()
        self._logs_path_layout.addWidget(self._logs_path_textbox)
        self._logs_path_layout.addWidget(self._logs_path_button)

        self._properties_layout = QFormLayout()
        self._properties_layout.addRow("Status:", self._status_label)
        self._properties_layout.addRow("Url:", self._url_label)
        self._properties_layout.addRow("Logs Dir:", self._logs_path_layout)

        self._properties_group = QGroupBox("Properties")
        self._properties_group.setLayout(self._properties_layout)

        self._launch_button = QPushButton("Launch")
        self._launch_button.clicked.connect(self.launch_tensorboard)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._properties_group)
        self._main_layout.addWidget(self._launch_button)

        self.setLayout(self._main_layout)

        self._update_states()

    def get_callbacks(self) -> List[Callback]:
        return []

    def launch_tensorboard(self):
        if self.tensorboard_status == "Running":
            LOGGER.info("Tensosboard is already Running.")
            self._update_states()
            return

        if not self._logs_path_textbox.text():
            LOGGER.warning("No Log Directory selected! Can't run Tensorboard.")
            return

        self.tensorboard_status = "Running"

        LOGGER.debug("Launching Tensorboard...")

        tb = program.TensorBoard()

        tb.configure(argv=[None, "--logdir", self._logs_path_textbox.text()])

        self.tensorboard_url = tb.launch()

        LOGGER.debug("Tensorboard launched!")

        self._update_states()

    def _pick_logs_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Logs directory")

        if dir_path:
            self._logs_path_textbox.setText(dir_path)
        else:
            LOGGER.info("Picking Log directory cancelled.")

    def _update_states(self):
        if self.tensorboard_status == "Stopped":
            self._launch_button.setEnabled(True)

        if self.tensorboard_status == "Running":
            self._launch_button.setEnabled(False)

        self._status_label.setText(self.tensorboard_status)
        self._url_label.setText(self.tensorboard_url)

    def sizeHint(self) -> "QSize":
        return QSize(400, 200)


TensorboardInstanceWidgetFactory = providers.Factory(TensorboardInstanceWidget)
