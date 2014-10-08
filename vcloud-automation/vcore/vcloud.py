#!/usr/bin/env python

__author__ = 'krishnaa'

import time
import optparse

from configobj import ConfigObj

from getToken import getToken
from getOrgs import getOrgs
from getVDC import getVDC
from getCatalog import getCatalog
from getCatalogItem import getCatalogItem
from getEntityDetails import getEntityDetails
from checkVAPP import checkVAPP
from deployVapp import deployVapp
from getVAPP import getVAPP
from poweroffVM import poweroffVM
from deleteVM import deleteVM
from taskStatus import taskStatus
from checkVM import checkVM
from processVM import processVM


def vcloud(options):

    config = ConfigObj(options.config_file)
    vapp_name = config['vapp']['name']
    vapp_desc = config['vapp']['description']
    vapp_poweron = config['vapp']['poweron']
    vapp_deploy = config['vapp']['deploy']
    url = config['vcloud']['url']
    login = config['vcloud']['login']
    passwd = config['vcloud']['passwd']
    vdc = config['vcloud']['vdc_name']
    catalog = config['vcloud']['catalog_name']
    vapp_template_name = config['vcloud']['vapp_template_name']
    token = getToken(url,login,passwd,'POST')
    orgs = getOrgs(url,token,'GET')


    for org in orgs:
        print "name: %s" % org['name']
        print "type: %s" % org['type']
        print "url: %s" % org['href']
        vdc_dict,catalog_dict = getVDC(org['href'], token, vdc, catalog)

    print "VDC details"
    print vdc_dict['href']
    print vdc_dict['name']
    print
    print "Catalog details"
    print catalog_dict['name']
    print catalog_dict['href']

    catalogItem_dict = getCatalog(catalog_dict['href'],token,'GET',vapp_template_name)
    #print catalogItem_dict

    vappi_dict = getCatalogItem(catalogItem_dict['href'],token,'GET')
    print "Catalog Item"
    #print vappi_dict
    print vappi_dict['href']
    print vappi_dict['name']

    getEntityDetails(vappi_dict['href'],token,'GET')
    #Check VAPP
    vapp_href,vapp_exist = checkVAPP(vapp_name,vdc_dict['href'],token,'GET')
    print vapp_exist
    if vapp_exist is False:
        vapp_href = deployVapp(vapp_name,vapp_desc,vapp_poweron,vapp_deploy,vdc_dict['href'],token,'POST',vappi_dict['href'])
        print vapp_href
        print "VAPP is currently under the process for creation..."
        vm_href,vm_name = getVAPP(vapp_href,token,'GET')
        print vm_href
        print "VAPP has been successfully created..."
        #poweroff the new VM
        print 'Undeploy VApp to poweroff VM...'
        status,task_href = poweroffVM(vm_href,token,'POST')

        while True:
            task_status = taskStatus(task_href,token,'GET')
            if task_status != 'success':
                print "Rechecking task status in 10secs..."
                time.sleep(10)
            else:
                break
        print 'poweroff vm: ',task_status

        #delete the deployed VM within VAPP
        print "Delete the new VM in the VApp..."
        task_href = deleteVM(vapp_name,vapp_href,vm_href,token,'POST')

        while True:
            task_status = taskStatus(task_href,token,'GET')
            if task_status != 'success':
                print "Rechecking task status in 10secs..."
                time.sleep(10)
            else:
                break
        print 'delete vm: ',task_status

    else:
        print "VApp already exists..."



    vdc_href = vappi_dict['href']
    print "Adding new VM"

    total_vm = config['vapp']['total_vm']
    i = 1
    while True:
        if i <= int(total_vm):

            vm = "vm_"+str(i)
            vm_name = config['vapp'][vm]['vm_name']
            vm_ip = config['vapp'][vm]['ipaddr']
            vm_network = config['vapp'][vm]['network']
            print vm_name
            vm_exist = checkVM(vm_name,vapp_href,token,'GET')
            if vm_exist is False:
                print "Building..."
                print "VM NAME: ", vm_name
                print "VM IP: ", vm_ip
                print "VM NETWORK: ", vm_network
                print "I am going to sleep for 20sec and then start processing the next VM....yawn.."
                time.sleep(20)
                processVM(vapp_name,vapp_desc,vapp_href,vdc_href,token,vm_name,vm_ip,vm_network)
            else:
                print "VM with that name already exists.."
                pass

        else:
            break
        i = i + 1

    print 'All operations complete...'

