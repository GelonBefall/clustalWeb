import os
import time
from flask import render_template, url_for, flash, redirect, request,send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from . import main
from .fastaOp import saveFasta
from .seqAli import clu

# 序列提交用表单类
class SeqForm(FlaskForm):
    seqName1 = StringField('序列名')
    seqData1 = TextAreaField('序列')
    seqName2 = StringField('序列名')
    seqData2 = TextAreaField('序列')
    seqSubmit = SubmitField('提交')
    seqFile = FileField('序列文件')


@main.route('/')
def space():
    return redirect(url_for('main.index'))

@main.route('/index', methods=['POST', 'GET'])
def index():
   # 表单类实例化
    SeqToForm = SeqForm()

    # 序列验证触发
    if SeqToForm.validate_on_submit():
    # if request.method == 'POST':
        workTime = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
        # 若上传文件存在
        # try :
        seqFile = request.files['seqFile']
        if seqFile.filename == '':
          seqName1 = SeqToForm.seqName1.data
          seqData1 = SeqToForm.seqData1.data
          seqName2 = SeqToForm.seqName2.data
          seqData2 = SeqToForm.seqData2.data
          if seqData1=='' or seqData2=='':
            return redirect(url_for('main.inputError'))
          else:
            seq1={seqName1:seqData1}
            seq2={seqName2:seqData2}
            saveFasta(workTime,seq1,seq2)
        else :
          fileName = "Sequences" + workTime + ".fasta"
          basepath = os.path.dirname(__file__)  # 当前文件所在路径
          uploadPath = os.path.join(basepath, 'history', fileName)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
          seqFile.save(uploadPath)
          flash("Upload success! ")
        

        # finally:
        return redirect(url_for('main.cluResult', workTime=workTime))
    return render_template('clustal.html', form=SeqToForm)

@main.route('/cluResult/<workTime>')
def cluResult(workTime):
  # try:
  alnOpt=clu(workTime)
  # print(alnOpt)
  basepath = os.path.dirname(__file__)
  alnName = "Aligned" + workTime + ".aln"
  alnPath = os.path.join(basepath, "./output/" + alnName)
  # except :
    # flash("Your input outlaw!")
  return render_template('clustalResult.html', output=alnOpt, alnName=alnName, alnPath=alnPath)

@main.route('/cluResultdownload<alnName>')
def alnDownload(alnName):
  basepath = os.path.dirname(__file__)
  # alnName = "Aligned" + workTime + ".aln"
  alnPath = os.path.join(basepath, "./output/") 
  return send_from_directory(alnPath, alnName, as_attachment=True)