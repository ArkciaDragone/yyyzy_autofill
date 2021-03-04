# YYYZY_Autofill 燕园云战疫自动填充

This software basically *repeats* yesterday's submission. Written purely in Python, it supports automated login and on/off campus form submission. This software has endured long-term emperical tests with correct outcomes.

此软件基本上*复制*昨天的提交。它完全用Python编写，支持自动登录和校内/校外表单提交。此软件经过长期测试，可以正确使用。

This software simulates most of the login operations to match browser behaviors. In order to prevent incorrect submissions due to modification of the form, different verification methods are designed.

此软件模拟了登陆时的大部分操作以吻合浏览器行为。为防止表单有变而产生误提交，设计了不同的验证方法。

How to use:
 - Fill the form manually once (to provide the software the data to repeat) and wait till tomorrow
 - Install the requirements: `pip install -r requirements.txt`
 - Run the file
 - Change the information and submit manually on demand

使用方法：
 - 在前一日手动填充一次表格（为此软件提供用于重复的数据）
 - 安装需求包：`pip install -r requirements.txt`
 - 运行py文件
 - 需要更改提交信息时，再进行手动填充

Note that this software assumes there is no case of leaving school. For that purpose a manual submission is required, and the next day the software will not repeat the previous day's submission but, for convenience, submit a new one with no leaving info.

请注意，此软件假定没有离校情况进行填充。如有此需要，需要手动提交，第二天此软件出于方便起见将不会重复前一天的提交，而提交一个没有离校的版本。

Multiple parameters can be supplied to control the behavior of the software. To see all the options available, run the file with `-h`. For example, it's a good idea to add the software to crontab with the `-y` parameter.

可以提供多个参数来控制此软件的行为。要查看所有可用选项，请使用`-h`参数运行该文件。例如，使用`-y`选项将软件添加到crontab是个好主意。

Student ID and password are stored locally in `private.json` in base64 encoding. Please protect this file because it is not encrypted even though it avoids storing the original values directly. If you do not wish to save the login info, please use the `-S` parameter.

学生ID和密码以base64编码存储在文件夹内的`private.json`中。请保护好此文件，因为尽管避免了直接存储原值，它也没有进行加密。如果不想保存登录信息，请使用`-S`参数。

*By using this software, you understand and agree that the author does not assume any responsibility for possible consequences. See the enclosed LICENSE for complete terms.*

*通过使用本软件，您理解并同意作者对可能的后果不承担任何责任。有关完整条款，请参阅随附的许可证。*