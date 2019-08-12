from argparse import ArgumentParser
from operator import itemgetter

import wmi


def parse_args():
    parser = ArgumentParser()
    sort_choices = ['pid', 'name', 'state', 'path']
    parser.add_argument('-s',
                        metavar='--sort',
                        action='store',
                        default='pid',
                        choices=sort_choices,
                        help="specify a sorting method: pid/name/state/path")
    parser.add_argument('-r',
                        action='store_true',
                        help="include this flag to reverse sort")
    return parser.parse_args()


def get_sorted_services(sort_by, reverse=False):
    return sorted(yield_services(), key=itemgetter(sort_by), reverse=reverse)


def yield_services():
    w = wmi.WMI()
    for s in w.Win32_Service(["Name", "ProcessId", "PathName", "State"]):
        yield {"pid": s.ProcessId,
               "state": s.State,
               "name": s.Name,
               "path": s.PathName or ''}


if __name__ == '__main__':
    args = parse_args()
    for s in get_sorted_services(args.s, args.r):
        line = "{pid:5} [{state[0]}] {name}  {path}".format(pid=s['pid'],
                                                            state=s['state'],
                                                            name=s['name'],
                                                            path=s['path'])
        print line
