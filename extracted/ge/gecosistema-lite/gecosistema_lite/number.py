# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        numbers.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     06/10/2017
# -------------------------------------------------------------------------------
import random, math


def randint(max=100):
    return random.randint(0, max)


def dist(p1, p2):
    """
    dist - euclidean distance
    """
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.sqrt(x ** 2 + y ** 2)


def cosx(p1, p2):
    """
    cosx - from points p1,p2
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx==0:
        return 0.0
    tgx = dy / dx
    sign = 1 if dx > 0 else -1
    return sign * 1.0 / (math.sqrt(1 + tgx ** 2))


def sinx(p1, p2):
    """
    sinx - from points p1,p2
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx==0:
        return 1.0
    tgx = dy / dx
    sign = 1 if dx > 0 else -1
    return sign * tgx / (math.sqrt(1 + tgx ** 2))


if __name__ == "__main__":
    pass
