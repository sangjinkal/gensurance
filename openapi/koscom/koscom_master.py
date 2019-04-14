import urllib.request
import urllib
import json
from webclient import WebClient
import http.client
import ast
import syslog
from koscom_base import Koscom
from insuranceCommon import getID, getDobConvert
import MySQLdb
import time
from dbconnect import connection
from MySQLdb import escape_string as thwart
from koscom_list import StockList
from koscom_listctl import StockListCtl

class KoscomMaster:
    def __init__(self,mode="read"):
        self.mode = mode
        self.issuecode = ''
        self.marketcode = ''
        self.id = ''
        self.trdDd = ''
        self.isuCd = ''
        self.isuSrtCd = ''
        self.isuKorAbbrv = ''
        self.secugrpId = ''
        self.mktWarnTpCd = ''
        self.govncExcelYn = ''
        self.admisuYn = ''
        self.haltYn = ''
        self.idxIndUpclssCd = ''
        self.idxIndMidclssCd = ''
        self.idxIndLwclssCd = ''
        self.mktcapScaleCd = ''
        self.mfindYn = ''
        self.smeYn = ''
        self.isuTrdvol = ''
        self.kospiYn = ''
        self.kospi100Yn = ''
        self.kospi50Yn = ''
        self.krxAutosSectidxYn = ''
        self.krxSemiconSectidxYn = ''
        self.krxBioSectidxYn = ''
        self.krxFncSectidxYn = ''
        self.krxEnergyChemSectidxYn = ''
        self.krxSteelSectidxYn = ''
        self.krxMediaCommSectidxYn = ''
        self.krxConstrSectidxYn = ''
        self.krxSecuSectidxYn = ''
        self.basPrc = 0
        self.prevddClsprc = 0
        self.prevddAccTrdvol = 0
        self.prevddAccTrdval = 0
        self.uplmtprc = 0
        self.lwlmtprc = 0
        self.sbPrc = 0
        self.parval = 0
        self.isuPrc = 0
        self.listDd = 0
        self.listShrs = 0
        self.arrantrdYn = ''
        self.creditOrdPosblYn = ''
        self.regulssQtyUnit = ''
        self.sriidxYn = ''
        self.krxInsuSectidxYn = ''
        self.krx100IsuYn = ''
        self.invstcautnRemndIsuYn = ''
        self.srttrmOverheatIsuTpCd = ''
        self.eps = 0
        self.per = 0
        self.bps = 0
        self.pbr = 0
        self.dps = 0
        self.divYd = 0
    def update_valid(self):
        c, conn = connection()
        try:
            cmd_temp = "update gensurance.tb_stock_master set valid = 'N' where valid ='Y'"
            if self.mode == "write":

                c.execute(cmd_temp)
            else:
                pass
            return {"flag": "success","desc":"ok"}
        except Exception as e :
            print (e)
            return {"flag": "fail", "desc": e}
        finally:
            c.close()
            conn.close()
    def set_value(self,kwargs):
        c, conn = connection()
        try:
            self.issuecode = kwargs.get('issuecode','')
            self.marketcode = kwargs.get('marketcode','')

            if self.mode =="write":
                self.id = getID("tb_stock_master")
            else:
                self.id= "001"
            #maxID = "001"
            self.trdDd = kwargs.get('trdDd','')
            self.isuCd = kwargs.get('isuCd','')
            self.isuSrtCd = kwargs.get('isuSrtCd','')
            self.isuKorAbbrv = kwargs.get('isuKorAbbrv','')
            self.secugrpId = kwargs.get('secugrpId','')
            self.mktWarnTpCd = kwargs.get('mktWarnTpCd','')
            self.govncExcelYn = kwargs.get('govncExcelYn','')
            self.admisuYn = kwargs.get('admisuYn','')
            self.haltYn = kwargs.get('haltYn','')
            self.idxIndUpclssCd = kwargs.get('idxIndUpclssCd','')
            self.idxIndMidclssCd = kwargs.get('idxIndMidclssCd','')
            self.idxIndLwclssCd = kwargs.get('idxIndLwclssCd','')
            self.mktcapScaleCd = kwargs.get('mktcapScaleCd','')
            self.mfindYn = kwargs.get('mfindYn','')
            self.smeYn = kwargs.get('smeYn','')
            self.isuTrdvol = kwargs.get('isuTrdvol','')
            self.kospiYn = kwargs.get('kospiYn','')
            self.kospi100Yn = kwargs.get('kospi100Yn','')
            self.kospi50Yn = kwargs.get('kospi50Yn','')
            self.krxAutosSectidxYn = kwargs.get('krxAutosSectidxYn','')
            self.krxSemiconSectidxYn = kwargs.get('krxSemiconSectidxYn','')
            self.krxBioSectidxYn = kwargs.get('krxBioSectidxYn','')
            self.krxFncSectidxYn = kwargs.get('krxFncSectidxYn','')
            self.krxEnergyChemSectidxYn = kwargs.get('krxEnergyChemSectidxYn','')
            self.krxSteelSectidxYn = kwargs.get('krxSteelSectidxYn','')
            self.krxMediaCommSectidxYn = kwargs.get('krxMediaCommSectidxYn','')
            self.krxConstrSectidxYn = kwargs.get('krxConstrSectidxYn','')
            self.krxSecuSectidxYn = kwargs.get('krxSecuSectidxYn','')
            self.krxShipSectidxYn = kwargs.get('krxShipSectidxYn','')
            self.basPrc = kwargs.get('basPrc',0)
            self.prevddClsprc = kwargs.get('prevddClsprc',0)
            self.prevddAccTrdvol = kwargs.get('prevddAccTrdvol',0)
            self.prevddAccTrdval = kwargs.get('prevddAccTrdval',0)
            self.uplmtprc = kwargs.get('uplmtprc',0)
            self.lwlmtprc = kwargs.get('lwlmtprc',0)
            self.sbPrc = kwargs.get('sbPrc',0)
            self.parval = kwargs.get('parval',0)
            self.isuPrc = kwargs.get('isuPrc',0)
            self.listDd = kwargs.get('listDd','')
            self.listShrs = kwargs.get('listShrs',0)
            self.arrantrdYn = kwargs.get('arrantrdYn','')
            self.creditOrdPosblYn = kwargs.get('creditOrdPosblYn','')
            self.regulssQtyUnit = kwargs.get('regulssQtyUnit',0)
            self.sriidxYn = kwargs.get('sriidxYn','')
            self.krxInsuSectidxYn = kwargs.get('krxInsuSectidxYn','')
            self.krx100IsuYn = kwargs.get('krx100IsuYn','')
            self.invstcautnRemndIsuYn = kwargs.get('invstcautnRemndIsuYn','')
            self.srttrmOverheatIsuTpCd = kwargs.get('srttrmOverheatIsuTpCd','')
            self.eps = kwargs.get('eps',0)
            self.per = kwargs.get('per',0)
            self.bps = kwargs.get('bps',0)
            self.pbr = kwargs.get('pbr',0)
            self.dps = kwargs.get('dps',0)
            self.divYd = kwargs.get('divYd',0)
            # for k, v in body_dict.items():``
            #     temp_trdDd = v.get("trdDd")


            cmd = "insert into gensurance.tb_stock_master"
            cmd = cmd + "(id, marketcode, issuecode, trdDd, isuCd, isuSrtCd, isuKorAbbrv, secugrpId, mktWarnTpCd, govncExcelYn,"
            cmd = cmd + "admisuYn, haltYn, idxIndUpclssCd, idxIndMidclssCd, idxIndLwclssCd, mktcapScaleCd, mfindYn,"
            cmd = cmd + "smeYn, isuTrdvol, kospiYn, kospi100Yn, kospi50Yn, krxAutosSectidxYn, krxSemiconSectidxYn,krxBioSectidxYn,krxFncSectidxYn,krxEnergyChemSectidxYn,"
            cmd = cmd + "krxSteelSectidxYn, krxMediaCommSectidxYn, krxConstrSectidxYn, krxSecuSectidxYn, krxShipSectidxYn,"
            cmd = cmd + "basPrc, prevddClsprc, prevddAccTrdvol, prevddAccTrdval, uplmtprc, lwlmtprc, sbPrc, parval,"
            cmd = cmd + "isuPrc, listDd, listShrs, arrantrdYn, creditOrdPosblYn, regulssQtyUnit, sriidxYn, krxInsuSectidxYn,"
            cmd = cmd + "krx100IsuYn, invstcautnRemndIsuYn, srttrmOverheatIsuTpCd, eps, per, bps, pbr, dps, divYd) "
            cmd = cmd + " values ("
            cmd = cmd + "'{id}', '{marketcode}', '{issuecode}','{trdDd}','{isuCd}','{isuSrtCd}','{isuKorAbbrv}','{secugrpId}','{mktWarnTpCd}','{govncExcelYn}',"
            cmd = cmd + "'{admisuYn}','{haltYn}','{idxIndUpclssCd}','{idxIndMidclssCd}','{idxIndLwclssCd}','{mktcapScaleCd}','{mfindYn}',"
            cmd = cmd + "'{smeYn}','{isuTrdvol}','{kospiYn}','{kospi100Yn}','{kospi50Yn}','{krxAutosSectidxYn}','{krxSemiconSectidxYn}','{krxBioSectidxYn}','{krxFncSectidxYn}','{krxEnergyChemSectidxYn}',"
            cmd = cmd + "'{krxSteelSectidxYn}','{krxMediaCommSectidxYn}','{krxConstrSectidxYn}','{krxSecuSectidxYn}','{krxShipSectidxYn}',"
            cmd = cmd + "{basPrc},{prevddClsprc},{prevddAccTrdvol},{prevddAccTrdval},{uplmtprc},{lwlmtprc},{sbPrc},{parval},"
            cmd = cmd + " {isuPrc},'{listDd}',{listShrs},'{arrantrdYn}','{creditOrdPosblYn}',{regulssQtyUnit},'{sriidxYn}','{krxInsuSectidxYn}',"
            cmd = cmd + "'{krx100IsuYn}','{invstcautnRemndIsuYn}','{srttrmOverheatIsuTpCd}',{eps},{per},{bps},{pbr},{dps},{divYd} )"
            sql = cmd.format (id=self.id, marketcode = self.marketcode, issuecode = self.issuecode,
            trdDd=self.trdDd,isuCd=self.isuCd,isuSrtCd=self.isuSrtCd,isuKorAbbrv=self.isuKorAbbrv,secugrpId=self.secugrpId,mktWarnTpCd=self.mktWarnTpCd,govncExcelYn=self.govncExcelYn,
            admisuYn=self.admisuYn,haltYn=self.haltYn,idxIndUpclssCd=self.idxIndUpclssCd,idxIndMidclssCd=self.idxIndMidclssCd,idxIndLwclssCd=self.idxIndLwclssCd,mktcapScaleCd=self.mktcapScaleCd,mfindYn=self.mfindYn,
            smeYn=self.smeYn,isuTrdvol=self.isuTrdvol,kospiYn=self.kospiYn,kospi100Yn=self.kospi100Yn,kospi50Yn=self.kospi50Yn,krxAutosSectidxYn=self.krxAutosSectidxYn,krxSemiconSectidxYn=self.krxSemiconSectidxYn,krxBioSectidxYn=self.krxBioSectidxYn,krxFncSectidxYn=self.krxFncSectidxYn,krxEnergyChemSectidxYn=self.krxEnergyChemSectidxYn,
            krxSteelSectidxYn=self.krxSteelSectidxYn,krxMediaCommSectidxYn=self.krxMediaCommSectidxYn,krxConstrSectidxYn=self.krxConstrSectidxYn,krxSecuSectidxYn=self.krxSecuSectidxYn,krxShipSectidxYn=self.krxShipSectidxYn,
            basPrc=self.basPrc,prevddClsprc=self.prevddClsprc,prevddAccTrdvol=self.prevddAccTrdvol,prevddAccTrdval=self.prevddAccTrdval,uplmtprc=self.uplmtprc,lwlmtprc=self.lwlmtprc,sbPrc=self.sbPrc,parval=self.parval,
            isuPrc=self.isuPrc,listDd=self.listDd,listShrs=self.listShrs,arrantrdYn=self.arrantrdYn,creditOrdPosblYn=self.creditOrdPosblYn,regulssQtyUnit=self.regulssQtyUnit,sriidxYn=self.sriidxYn,krxInsuSectidxYn=self.krxInsuSectidxYn,
            krx100IsuYn=self.krx100IsuYn,invstcautnRemndIsuYn=self.invstcautnRemndIsuYn,srttrmOverheatIsuTpCd=self.srttrmOverheatIsuTpCd,eps=self.eps,per=self.per,bps=self.bps,pbr=self.pbr,dps=self.dps,divYd=self.divYd)
            if self.mode == "write":
                c.execute(sql)
                conn.commit()
            else:
                print(sql)


        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            c.close()
            conn.close()
    def get_value_all(self):
        c,conn = connection()
        try:
            cmd = "select "
            cmd = cmd + "id, marketcode, issuecode, trdDd, isuCd, isuSrtCd, isuKorAbbrv, secugrpId, mktWarnTpCd, govncExcelYn,"
            cmd = cmd + "admisuYn, haltYn, idxIndUpclssCd, idxIndMidclssCd, idxIndLwclssCd, mktcapScaleCd, mfindYn,"
            cmd = cmd + "smeYn, isuTrdvol, kospiYn, kospi100Yn, kospi50Yn, krxAutosSectidxYn, krxSemiconSectidxYn,krxBioSectidxYn,krxFncSectidxYn,krxEnergyChemSectidxYn,"
            cmd = cmd + "krxSteelSectidxYn, krxMediaCommSectidxYn, krxConstrSectidxYn, krxSecuSectidxYn, krxShipSectidxYn,"
            cmd = cmd + "basPrc, prevddClsprc, prevddAccTrdvol, prevddAccTrdval, uplmtprc, lwlmtprc, sbPrc, parval,"
            cmd = cmd + "isuPrc, listDd, listShrs, arrantrdYn, creditOrdPosblYn, regulssQtyUnit, sriidxYn, krxInsuSectidxYn,"
            cmd = cmd + "krx100IsuYn, invstcautnRemndIsuYn, srttrmOverheatIsuTpCd, eps, per, bps, pbr, dps, divYd"
            cmd = cmd + " from gensurance.tb_stock_master where valid = 'Y'"

            c.execute(cmd)
            rows = c.fetchall()
            List = []
            for row in rows:
                maxID = row[0]
                marketcode = row[1]
                issuecode = row[2]
                trdDd = row[3]
                isuCd = row[4]
                isuSrtCd = row[5]
                isuKorAbbrv = row[6]
                secugrpId = row[7]
                mktWarnTpCd = row[8]
                govncExcelYn = row[9]
                admisuYn = row[10]
                haltYn = row[11]
                idxIndUpclssCd = row[12]
                idxIndMidclssCd = row[13]
                idxIndLwclssCd = row[14]
                mktcapScaleCd = row[15]
                mfindYn = row[16]
                smeYn = row[17]
                isuTrdvol = row[18]
                kospiYn = row[19]
                kospi100Yn = row[20]
                kospi50Yn = row[21]
                krxAutosSectidxYn = row[22]
                krxSemiconSectidxYn = row[23]
                krxBioSectidxYn = row[24]
                krxFncSectidxYn = row[25]
                krxEnergyChemSectidxYn = row[26]
                krxSteelSectidxYn = row[27]
                krxMediaCommSectidxYn = row[28]
                krxConstrSectidxYn = row[29]
                krxSecuSectidxYn = row[30]
                krxShipSectidxYn = row[31]
                basPrc = row[32]
                prevddClsprc = row[33]
                prevddAccTrdvol = row[34]
                prevddAccTrdval = row[35]
                uplmtprc = row[36]
                lwlmtprc = row[37]
                sbPrc = row[38]
                parval = row[39]
                isuPrc = row[40]
                listDd = row[41]
                listShrs = row[42]
                arrantrdYn = row[43]
                creditOrdPosblYn = row[44]
                regulssQtyUnit = row[45]
                sriidxYn = row[46]
                krxInsuSectidxYn = row[47]
                krx100IsuYn = row[48]
                invstcautnRemndIsuYn = row[49]
                srttrmOverheatIsuTpCd = row[50]
                eps = row[51]
                per = row[52]
                bps = row[53]
                pbr = row[54]
                dps = row[55]
                divYd = row[56]
                kwargs = {
                'id':maxID, 'marketcode' : marketcode, 'issuecode' : issuecode,
                'trdDd':trdDd,'isuCd':isuCd,'isuSrtCd':isuSrtCd,'isuKorAbbrv':isuKorAbbrv,'secugrpId':secugrpId,'mktWarnTpCd':mktWarnTpCd,'govncExcelYn':govncExcelYn,
                'admisuYn':admisuYn,'haltYn':haltYn,'idxIndUpclssCd':idxIndUpclssCd,'idxIndMidclssCd':idxIndMidclssCd,'idxIndLwclssCd':idxIndLwclssCd,'mktcapScaleCd':mktcapScaleCd,'mfindYn':mfindYn,
                'smeYn':smeYn,'isuTrdvol':isuTrdvol,'kospiYn':kospiYn,'kospi100Yn':kospi100Yn,'kospi50Yn':kospi50Yn,'krxAutosSectidxYn':krxAutosSectidxYn,'krxSemiconSectidxYn':krxSemiconSectidxYn,'krxBioSectidxYn':krxBioSectidxYn,'krxFncSectidxYn':krxFncSectidxYn,'krxEnergyChemSectidxYn':krxEnergyChemSectidxYn,
                'krxSteelSectidxYn':krxSteelSectidxYn,'krxMediaCommSectidxYn':krxMediaCommSectidxYn,'krxConstrSectidxYn':krxConstrSectidxYn,'krxSecuSectidxYn':krxSecuSectidxYn,'krxShipSectidxYn':krxShipSectidxYn,
                'basPrc':basPrc,'prevddClsprc':prevddClsprc,'prevddAccTrdvol':prevddAccTrdvol,'prevddAccTrdval':prevddAccTrdval,'uplmtprc':uplmtprc,'lwlmtprc':lwlmtprc,'sbPrc':sbPrc,'parval':parval,
                'isuPrc':isuPrc,'listDd':listDd,'listShrs':listShrs,'arrantrdYn':arrantrdYn,'creditOrdPosblYn':creditOrdPosblYn,'regulssQtyUnit':regulssQtyUnit,'sriidxYn':sriidxYn,'krxInsuSectidxYn':krxInsuSectidxYn,
                'krx100IsuYn':krx100IsuYn,'invstcautnRemndIsuYn':invstcautnRemndIsuYn,'srttrmOverheatIsuTpCd':srttrmOverheatIsuTpCd,'eps':eps,'per':per,'bps':bps,'pbr':pbr,'dps':dps,'divYd':divYd
                }
                List.append(kwargs)
            return List
        except Exception as e:
            return []
        finally:
            c.close()
            conn.close()
    def get_value(self,issuecode = "005930"):
        c,conn = connection()
        try:
            cmd = "select "
            cmd = cmd + "id, marketcode, issuecode, trdDd, isuCd, isuSrtCd, isuKorAbbrv, secugrpId, mktWarnTpCd, govncExcelYn,"
            cmd = cmd + "admisuYn, haltYn, idxIndUpclssCd, idxIndMidclssCd, idxIndLwclssCd, mktcapScaleCd, mfindYn,"
            cmd = cmd + "smeYn, isuTrdvol, kospiYn, kospi100Yn, kospi50Yn, krxAutosSectidxYn, krxSemiconSectidxYn,krxBioSectidxYn,krxFncSectidxYn,krxEnergyChemSectidxYn,"
            cmd = cmd + "krxSteelSectidxYn, krxMediaCommSectidxYn, krxConstrSectidxYn, krxSecuSectidxYn, krxShipSectidxYn,"
            cmd = cmd + "basPrc, prevddClsprc, prevddAccTrdvol, prevddAccTrdval, uplmtprc, lwlmtprc, sbPrc, parval,"
            cmd = cmd + "isuPrc, listDd, listShrs, arrantrdYn, creditOrdPosblYn, regulssQtyUnit, sriidxYn, krxInsuSectidxYn,"
            cmd = cmd + "krx100IsuYn, invstcautnRemndIsuYn, srttrmOverheatIsuTpCd, eps, per, bps, pbr, dps, divYd"
            cmd = cmd + " from gensurance.tb_stock_master where valid = 'Y'"
            cmd = cmd + " and issuecode = '{issuecode}' "
            sql = cmd.format (issuecode=issuecode)

            c.execute(sql)
            row = c.fetchone()

            maxID = row[0]
            marketcode = row[1]
            issuecode = row[2]
            trdDd = row[3]
            isuCd = row[4]
            isuSrtCd = row[5]
            isuKorAbbrv = row[6]
            secugrpId = row[7]
            mktWarnTpCd = row[8]
            govncExcelYn = row[9]
            admisuYn = row[10]
            haltYn = row[11]
            idxIndUpclssCd = row[12]
            idxIndMidclssCd = row[13]
            idxIndLwclssCd = row[14]
            mktcapScaleCd = row[15]
            mfindYn = row[16]
            smeYn = row[17]
            isuTrdvol = row[18]
            kospiYn = row[19]
            kospi100Yn = row[20]
            kospi50Yn = row[21]
            krxAutosSectidxYn = row[22]
            krxSemiconSectidxYn = row[23]
            krxBioSectidxYn = row[24]
            krxFncSectidxYn = row[25]
            krxEnergyChemSectidxYn = row[26]
            krxSteelSectidxYn = row[27]
            krxMediaCommSectidxYn = row[28]
            krxConstrSectidxYn = row[29]
            krxSecuSectidxYn = row[30]
            krxShipSectidxYn = row[31]
            basPrc = row[32]
            prevddClsprc = row[33]
            prevddAccTrdvol = row[34]
            prevddAccTrdval = row[35]
            uplmtprc = row[36]
            lwlmtprc = row[37]
            sbPrc = row[38]
            parval = row[39]
            isuPrc = row[40]
            listDd = row[41]
            listShrs = row[42]
            arrantrdYn = row[43]
            creditOrdPosblYn = row[44]
            regulssQtyUnit = row[45]
            sriidxYn = row[46]
            krxInsuSectidxYn = row[47]
            krx100IsuYn = row[48]
            invstcautnRemndIsuYn = row[49]
            srttrmOverheatIsuTpCd = row[50]
            eps = row[51]
            per = row[52]
            bps = row[53]
            pbr = row[54]
            dps = row[55]
            divYd = row[56]
            kwargs = {
            'id':maxID, 'marketcode' : marketcode, 'issuecode' : issuecode,
            'trdDd':trdDd,'isuCd':isuCd,'isuSrtCd':isuSrtCd,'isuKorAbbrv':isuKorAbbrv,'secugrpId':secugrpId,'mktWarnTpCd':mktWarnTpCd,'govncExcelYn':govncExcelYn,
            'admisuYn':admisuYn,'haltYn':haltYn,'idxIndUpclssCd':idxIndUpclssCd,'idxIndMidclssCd':idxIndMidclssCd,'idxIndLwclssCd':idxIndLwclssCd,'mktcapScaleCd':mktcapScaleCd,'mfindYn':mfindYn,
            'smeYn':smeYn,'isuTrdvol':isuTrdvol,'kospiYn':kospiYn,'kospi100Yn':kospi100Yn,'kospi50Yn':kospi50Yn,'krxAutosSectidxYn':krxAutosSectidxYn,'krxSemiconSectidxYn':krxSemiconSectidxYn,'krxBioSectidxYn':krxBioSectidxYn,'krxFncSectidxYn':krxFncSectidxYn,'krxEnergyChemSectidxYn':krxEnergyChemSectidxYn,
            'krxSteelSectidxYn':krxSteelSectidxYn,'krxMediaCommSectidxYn':krxMediaCommSectidxYn,'krxConstrSectidxYn':krxConstrSectidxYn,'krxSecuSectidxYn':krxSecuSectidxYn,'krxShipSectidxYn':krxShipSectidxYn,
            'basPrc':basPrc,'prevddClsprc':prevddClsprc,'prevddAccTrdvol':prevddAccTrdvol,'prevddAccTrdval':prevddAccTrdval,'uplmtprc':uplmtprc,'lwlmtprc':lwlmtprc,'sbPrc':sbPrc,'parval':parval,
            'isuPrc':isuPrc,'listDd':listDd,'listShrs':listShrs,'arrantrdYn':arrantrdYn,'creditOrdPosblYn':creditOrdPosblYn,'regulssQtyUnit':regulssQtyUnit,'sriidxYn':sriidxYn,'krxInsuSectidxYn':krxInsuSectidxYn,
            'krx100IsuYn':krx100IsuYn,'invstcautnRemndIsuYn':invstcautnRemndIsuYn,'srttrmOverheatIsuTpCd':srttrmOverheatIsuTpCd,'eps':eps,'per':per,'bps':bps,'pbr':pbr,'dps':dps,'divYd':divYd
            }


            return kwargs
        except Exception as e:
            return {"error":e}
        finally:
            c.close()
            conn.close()

class KoscomMasterCtl:
    def __init__(self,mode="read",marketcode = "kospi"):
        self.mode = mode
        self.marketcode = marketcode

    def process_run(self):
        issuecode_temp = "005010"
        a = StockListCtl("read")

        dict_temp = a.get_value_all()
        #mode = "write"
        List = dict_temp.get("stock_list", [])
        totalcnt = len(List)
        cnt = 0
        c = KoscomMaster(self.mode)
        c.update_valid()
        for dict_temp1 in List:
            cnt = cnt + 1
            issuecode = dict_temp1.get("isuSrtCd",issuecode_temp)
            if mode == "write":
                print("inserting (" + issuecode + " - " + str(cnt) + "/" + str(totalcnt) + ")......")

            body_basic = {"issuecode":issuecode, "marketcode":self.marketcode}
            body_dict_temp = Koscom.get_stock_master(issuecode)

            body_dict = body_dict_temp.get("master", {})
            body_dict.update(body_basic)

            b = KoscomMaster(self.mode)
            b.set_value(body_dict)

    def get_value_all(self):
        process_name = "master"
        t = KoscomMaster(self.mode)
        List = t.get_value_all()
        return {process_name: List}

    def get_value(self,issuecode):
        process_name = "master"
        t= KoscomMaster(self.mode)
        Dict = t.get_value(issuecode)
        return {process_name: Dict}

if __name__ == "__main__" :

    mode = "write"
    issuecode = "005930"
    marketcode = "kospi"
    d=KoscomMasterCtl(mode,marketcode)
    d.process_run()

    #a=d.get_value(issuecode)

    #print(a)
