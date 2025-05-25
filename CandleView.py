# -*- coding: UTF-8 -*-
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt6.QtCore import QDir
import finplot as fplt
import sys

class CandleView(QWidget):
    def __init__(self):
        super(CandleView, self).__init__()
        ax0,ax1,ax2,ax3 = fplt.create_plot(rows=4)
        self.axs = [ax0, ax1, ax2, ax3]
        layout = QHBoxLayout()
        layout.addWidget(self.axs[0].vb.win)
        self.setLayout(layout)
        self.setWindowTitle("CandleView")

    def update_datas(self, datas):
        self.draw_candles(datas)
        self.draw_volume(datas)
        self.draw_boll(datas)
        self.draw_macd(datas)
        fplt.refresh()

    def draw_candles(self, datas):
        price = datas[['date', 'open', 'close', 'high', 'low']].set_index('date')

        ax = self.axs[0]
        fplt.candlestick_ochl(price, ax=ax)

        price['ma5'] = price.close.rolling(5).mean()
        fplt.plot(price['ma5'], ax=ax, legend='ma5', color='#00ff00')

        price['ma10'] = price.close.rolling(10).mean()
        fplt.plot(price['ma10'], ax=ax, legend='ma10', color='#ff0000')

        price['ma20'] = price.close.rolling(20).mean()
        fplt.plot(price['ma20'], ax=ax, legend='ma20', color='#0000ff')

    def draw_volume(self, datas):
        price = datas[['date', 'open', 'close', 'volume']].set_index('date')
        fplt.volume_ocv(price, ax=self.axs[1], colorfunc=fplt.strength_colorfilter)

    def draw_macd(self, datas):
        price = datas[['date', 'open', 'close']].reset_index()
        macd = price.close.ewm(span=12).mean() - datas.close.ewm(span=26).mean()
        signal = macd.ewm(span=9).mean()
        price['macd_diff'] = macd - signal

        ax = self.axs[2]
        fplt.volume_ocv(price[['date','open','close','macd_diff']].set_index('date'), ax=ax, colorfunc=fplt.strength_colorfilter)
        fplt.plot(macd, ax=ax, legend='MACD')
        fplt.plot(signal, ax=ax, legend='Signal')

    def draw_boll(self, datas):
        price = datas[['date', 'open', 'close', 'high', 'low']].set_index('date')

        ax = self.axs[3]
        fplt.candlestick_ochl(price, ax=ax)

        ma20 = price.close.rolling(20).mean()
        stddev = price.close.rolling(20).std()
        price['boll_hi'] = ma20 + 2.0 * stddev
        price['boll_lo'] = ma20 - 2.0 * stddev

        fplt.plot(ma20, ax=ax, legend='ma20', color='#0000ff')
        fplt.plot(price['boll_hi'], color='#964B00', ax=ax)
        fplt.plot(price['boll_lo'], color='#964B00', ax=ax)

if __name__ == "__main__":
    QDir.addSearchPath('images', '../images/')
    app = QApplication(sys.argv)
    app.setApplicationName("DataWindow")

    form = CandleView()
    form.showMaximized()

    app.exec()
