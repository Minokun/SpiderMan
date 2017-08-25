__author__ = "Minok"

from scrapy.cmdline import execute

import sys
import os
file_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(file_path)
execute(["scrapy","crawl","zhihu"])