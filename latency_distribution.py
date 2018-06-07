from collections import defaultdict


class LatencyDistribution(object):
    def __init__(self, arr):
        self.arr = arr
        self.avgTotal = 0
        self.statusCodeDist = {}
        self.errorDist = {}
        self.fastest = None
        self.slowest = None
        self.average = None
        self.avgTotal = 0
        self.lats = []

    def proc(self):
        for a in self.arr:
            status_code = a['status_code']
            print status_code
            print a['response']['time_used']
            if 'response' in a and 'time_used' in a['response']:
                time_used = float(a['response']['time_used'])
                self.lats.append(time_used)
                self.avgTotal += float(time_used)
            if status_code not in self.statusCodeDist:
                self.statusCodeDist[status_code] = 1
            else:
                self.statusCodeDist[status_code] += 1

        self.average = self.avgTotal / len(self.lats)
        self.lats = sorted(self.lats)
        self.fastest = self.lats[0]
        self.slowest = self.lats[len(self.lats) - 1]
        self.finalize()

    def finalize(self):
        print "\nSummary:\n"
        print "\tCount: " + str(len(self.arr))
        print "\tSlowest: " + str(self.slowest)
        print "\tFastest: " + str(self.fastest)
        print "\tAverage: " + str(self.average)
        pctls = [10, 25, 50, 75, 90, 95, 99]
        data = defaultdict(int)
        j = 0
        for i in range(0, len(self.lats)):
            if j >= len(pctls):
                break
            current = float(i * 100) / len(self.lats)
            if current >= pctls[j]:
                data[pctls[j]] = self.lats[i]
                j += 1
        print "\nLatency distribution:\n"
        for i in pctls:
            if data[i] > 0:
                print "\t%s%% in %4.4f s" % (i, data[i])

        print "\nStatus Code:\n"
        for key, value in self.statusCodeDist.iteritems():
            print "\t[%s]\t%s" % (key, value)
