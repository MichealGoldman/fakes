"""
        Title: find_fakes
        Author: Harold Goldman
        Email: hgold90@entergy.com
        Date: 9/15/2017
        Description: Python program lists known fake packages from pypi
                     and prompts user for removal suing pip.
"""

from __future__ import print_function
import sys
import os
import argparse
import subprocess
from collections import OrderedDict
import pip


def get_packages():
    """
    get packages installed by pip
    """
    print("\t1. Creating list of installed pypi packages.")
    return sorted(["{}".format(i.key) for i in
                   pip.get_installed_distributions()])


def get_fakes(infile):
    """
    get list of know pypi fakes
    """
    print('\t2. Creating list of fake pypi packages.')
    with open(infile, 'r') as inf:
        return inf.read().replace(" ", "").split(",")


def search_packages(packages, fakes):
    """
    create a list of fake packages found
    """
    print("\t3. Searching installed packages for fake packages.")
    founds = []
    for fake in fakes:
        if fake in packages:
            print("\t\tLocated fake pypi "
                  "package {} on your system.".format(fake))
            founds.append(fake)
    return founds


def remove_packages(founds):
    """
    prompt the user, if they agree remove package
    """
    removed = OrderedDict()
    present = OrderedDict()

    if not founds:
        return False
    else:
        print("\t4. Auto removal of fake pypi packages using pip.")
        for fake in founds:
            if sys.version_info >= (3, 0):
                ans = input("\t\tUninstall {0} from system? Y/N   "
                            .format(fake)).upper()
            else:
                ans = raw_input("\t\tUninstall {0} from system? Y/N   "
                                .format(fake)).upper()

            while ans != 'Y' and ans != 'N' and ans != 'Q':
                if sys.version_info >= (3, 0):
                    ans = input("\t\t..Please answer Y or N, or "
                                "Q to quit. Y/N/Q  ").upper()
                else:
                    ans = raw_input("\t\t..Please answer Y or N, or "
                                    "Q to quit. Y/N/Q  ").upper()
            if ans == 'Y':
                print('\t\tUsing pip to uninstall {}.'.format(fake))
                cmd = "pip uninstall -y {}".format(fake)
                subprocess.call(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
                removed[fake] = True
            elif ans == 'N':
                present[fake] = False
            else:
                sys.exit(0)
    return([removed, present])


def report_fakes(removed):
    """
    generate a report of
    fakes found and removed
    """
    if removed is False:
        print('\t4. Report:')
        print("\t\tNo known fake pypi packages were found on your system.")
        sys.exit(0)
    else:
        print('\t5. Report:')
    if removed[0]:
        print("\t\tThe following fake pypi packages have been removed:")
        for key in removed[0].keys():
            print("\t\t\t{}".format(key))
    if removed[1]:
        print("\t\tThe following fake "
              "pypi packages are present, please remove:")
        for key in removed[1].keys():
            print("\t\t\t{}".format(key))
    sys.exit(0)


def get_args():
    """
    get args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="the csv file containing the fake pypi packages",
                        type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


if __name__ == "__main__":
    ARGS = get_args()
    print("\n")
    if os.path.isfile(ARGS.filename):
        report_fakes(remove_packages(
            search_packages(
                get_packages(),
                get_fakes(ARGS.filename))))
    else:
        print("\t\tInvalid filename provided, "
              "please provide a valid filename.")
