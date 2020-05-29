import urllib.request
import re


def generate_modes_list(freqs=None):
    index_html = urllib.request.urlopen('http://www.tinyvga.com/vga-timing').read()
    index_re = re.compile('<a href=\"(/vga-timing/(\d{3,4})x(\d{3,4})@(\d{2,3})Hz)\">')
    modes = index_re.findall(str(index_html))
    mode_re = re.compile('<td.*?>(.*?)</td>')
    num_re = re.compile('[\.\d]+')
    for url, w, h, freq in modes:
        if freqs is not None and freq not in freqs:
            continue
        mode_html = urllib.request.urlopen('http://www.tinyvga.com/' + url).read()
        items = mode_re.findall(str(mode_html))
        data = {}
        for i in range(0, 6, 2):
            data[items[i]] = num_re.findall(items[i + 1])[0]
        for i in range(6, len(items), 3):
            dim = 'h' if i <= 18 else 'v'
            value = num_re.findall(items[i + 1])
            if len(value) == 0:
                continue
            data[dim + items[i]] = value[0]
        print('; {}x{}@{}Hz'.format(w, h, freq))
        print('; video_mode=', end='')
        print(data['hVisible area'], end='')
        print(',' + data['hFront porch'], end='')
        print(',' + data['hSync pulse'], end='')
        print(',' + data['hBack porch'], end='')
        print(',' + data['vVisible area'], end='')
        print(',' + data['vFront porch'], end='')
        print(',' + data['vSync pulse'], end='')
        print(',' + data['vBack porch'], end='')
        print(',' + str(int(float(data['Pixel freq.']) * 1000)), end='')
        print('')


if __name__ == '__main__':
    generate_modes_list()
