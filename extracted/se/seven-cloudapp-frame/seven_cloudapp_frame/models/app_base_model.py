# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-28 09:54:51
@LastEditTime: 2025-03-19 17:52:04
@LastEditors: HuangJianYi
@Description: 
"""
from decimal import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.top_base_model import *
from seven_cloudapp_frame.models.seven_model import *
from seven_cloudapp_frame.models.db_models.app.app_info_model import *
from seven_cloudapp_frame.models.db_models.base.base_info_model import *
from seven_cloudapp_frame.models.db_models.friend.friend_link_model import *
from seven_cloudapp_frame.models.db_models.product.product_price_model import *
from seven_cloudapp_frame.models.db_models.tao.tao_login_log_model import *
from seven_cloudapp_frame.models.db_models.version.version_info_model import *
from seven_cloudapp_frame.models.db_models.dict.dict_info_model import *
from seven_cloudapp_frame.models.db_models.app.app_relation_model import *
from seven_cloudapp_frame.models.db_models.app.app_template_model import *

class AppBaseModel():
    """
    :description: 应用信息业务模型
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def get_app_id(self, store_name, template_id=""):
        """
        :description: 获取应用标识
        :param store_name:店铺名称
        :param template_id:模板UD
        :return app_id
        :last_editors: HuangJianYi
        """
        app_id = ""
        condition_where = ConditionWhere()
        condition_where.add_condition("store_name=%s")
        params = [store_name]
        if template_id:
            condition_where.add_condition("template_id=%s")
            params.append(template_id)
        app_info_dict = AppInfoModel(context=self.context, is_auto=True).get_cache_dict(condition_where.to_string(), limit="1", field="app_id", params=params)
        if app_info_dict:
            app_id = app_info_dict["app_id"]
        return app_id

    def get_app_info_dict(self, app_id, is_cache=True, field="*"):
        """
        :description: 获取应用信息
        :param app_id: 应用标识
        :param is_cache: 是否缓存
        :param field: 查询字段
        :return: 返回应用信息
        :last_editors: HuangJianYi
        """
        app_info_model = AppInfoModel(context=self.context, is_auto=True)
        if is_cache:
            dependency_key = DependencyKey.app_info(app_id)
            return app_info_model.get_cache_dict(where="app_id=%s",limit="1", field=field, params=[app_id],dependency_key=dependency_key)
        else:
            return app_info_model.get_dict(where="app_id=%s", limit="1",field=field, params=[app_id])

    def get_app_expire(self,app_id):
        """
        :description: 获取小程序是否过期未续费
        :param app_id: 应用标识
        :return 1过期0未过期
        :last_editors: HuangJianYi
        """
        now_date = SevenHelper.get_now_datetime()
        invoke_result_data = InvokeResultData()
        app_info_dict = self.get_app_info_dict(app_id)
        if not app_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "小程序不存在"
            return invoke_result_data
        result = {}
        app_info_dict["expiration_date"] = str(app_info_dict["expiration_date"])
        if app_info_dict["expiration_date"] == "1900-01-01 00:00:00":
            result["is_expire"] = 0
        elif now_date > app_info_dict["expiration_date"]:
            result["is_expire"] = 1
        else:
            result["is_expire"] = 0
        invoke_result_data.data = result
        return invoke_result_data

    def get_left_navigation(self, user_nick, access_token, app_key, app_secret, app_id=""):
        """
        :description: 获取左侧导航
        :param user_nick: 用户昵称
        :param app_key: app_key
        :param app_secret: app_secret
        :param access_token: access_token
        :param app_id: 应用标识
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        store_user_nick = user_nick.split(':')[0]
        if not store_user_nick:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，请先授权登录"
            return invoke_result_data
        base_info_dict = BaseInfoModel(context=self.context, is_auto=True).get_dict()
        if not base_info_dict:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "基础信息不存在"
            return invoke_result_data

        app_info_dict = None
        if app_id:
            app_info_dict = self.get_app_info_dict(app_id)

        # 左上角信息
        info = {}
        info["company"] = "天志互联"
        info["miniappName"] = base_info_dict["product_name"]
        info["logo"] = base_info_dict["product_icon"]
        info["client_now_ver"] = app_info_dict["template_ver"] if app_info_dict else ""

        # 左边底部菜单
        helper_info = {}
        helper_info["customer_service"] = base_info_dict["customer_service"]
        helper_info["video_url"] = base_info_dict["video_url"]
        helper_info["study_url"] = base_info_dict["study_url"]
        helper_info["is_remind_phone"] = base_info_dict["is_remind_phone"]
        helper_info["phone"] = ""

        # 过期时间
        renew_info = {}
        renew_info["surplus_day"] = 0
        dead_date = ""
        if app_info_dict:
            helper_info["phone"] = app_info_dict["app_telephone"]
            dead_date = app_info_dict["expiration_date"]
        else:
            top_base_model = TopBaseModel(context=self.context)
            invoke_result_data = top_base_model.get_dead_date(store_user_nick,access_token, app_key, app_secret)
            if invoke_result_data.success == False:
                return invoke_result_data
            dead_date = invoke_result_data.data
        renew_info["dead_date"] = dead_date
        if dead_date != "expire":
            renew_info["surplus_day"] = TimeHelper.difference_days(dead_date, SevenHelper.get_now_datetime())
        data = {}
        data["app_info"] = info
        data["helper_info"] = helper_info
        data["renew_info"] = renew_info

        product_price_model = ProductPriceModel(context=self.context, is_auto=True)
        now_date = SevenHelper.get_now_datetime()
        product_price = product_price_model.get_cache_entity(where="%s>=begin_time and %s<=end_time and is_release=1",order_by="create_time desc",params=[now_date,now_date])
        base_info = {}
        # 把string转成数组对象
        base_info["update_function"] = SevenHelper.json_loads(base_info_dict["update_function"]) if base_info_dict["update_function"] else []
        base_info["update_function_b"] = SevenHelper.json_loads(base_info_dict["update_function_b"]) if base_info_dict["update_function_b"] else []
        base_info["decoration_poster_list"] = SevenHelper.json_loads(base_info_dict["decoration_poster_json"]) if base_info_dict["decoration_poster_json"] else []
        base_info["menu_config_list"] = SevenHelper.json_loads(base_info_dict["menu_config_json"]) if base_info_dict["menu_config_json"] else []
        base_info["product_price_list"] = SevenHelper.json_loads(product_price.content) if product_price else []
        base_info["server_ver"] = base_info_dict["server_ver"]
        base_info["client_ver"] = base_info_dict["client_ver"]
        base_info["is_force_update"] = base_info_dict["is_force_update"]
        helper_info["is_force_phone"] = base_info_dict["is_force_phone"]

        #配置文件指定账号升级
        test_config = share_config.get_value("test_config",{})
        test_client_ver = test_config.get("client_ver","")
        if test_client_ver and store_user_nick and store_user_nick == test_config.get("user_nick",""):
            base_info["client_ver"] = test_client_ver
        else:
            #中台指定账号升级
            version_info = VersionInfoModel(context=self.context, is_auto=True).get_entity(where="type_id=1",order_by="id desc")
            if version_info:
                if version_info.update_scope == 2 and version_info.white_lists:
                    white_lists = SevenHelper.json_loads(version_info.white_lists)
                    if isinstance(white_lists, str):
                        white_lists = white_lists.split(',')
                    if store_user_nick in white_lists:
                        base_info["client_ver"] = version_info.version_number
        
        # 如果存在项目版本号，则替换掉client_ver
        if base_info_dict["project_ver"]:
            base_info["client_ver"] = base_info_dict["project_ver"] # 要升级的版本号
            data["app_info"]["client_now_ver"] = app_info_dict["project_ver"] # 当前版本号

        data["base_info"] = base_info


        
        # if is_multiple == 1:
        #     relation_app_ver_list = []
        #     app_template_model = AppTemplateModel(context=self.context)
        #     app_template_dict_list = app_template_model.get_dict_list(field="template_id,client_ver,update_function")
        #     if len(app_template_dict_list) > 0:
        #         app_info_model = AppInfoModel(context=self.context)
        #         app_info_dict_list = app_info_model.get_dict_list("store_user_nick=%s", field="template_id,template_ver", params=[store_user_nick])
        #         for app_template_dict in app_template_dict_list:
        #             app_info_dict_list = [item for item in app_info_dict_list if item["template_id"] == app_template_dict["template_id"]]
        #             app_info_dict = app_info_dict_list[0] if len(app_info_dict_list) > 0 else None
        #             other_app_ver = {}
        #             other_app_ver["client_now_ver"] =  app_info_dict["template_ver"] if app_info_dict else ""
        #             other_app_ver["client_ver"] = app_template_dict["client_ver"]
        #             other_app_ver["update_function"] = app_template_dict["update_function"]
        #             relation_app_ver_list.append(other_app_ver)
                
        #     data["relation_app_ver_list"] = relation_app_ver_list

        invoke_result_data.data = data
        return invoke_result_data

    def get_app_info_result(self, user_nick, open_id, access_token, app_key, app_secret, main_user_open_id=""):
        """
        :description: 获取小程序信息
        :param user_nick:用户昵称
        :param open_id:open_id
        :param access_token: access_token
        :param app_key:app_key
        :param app_secret: app_secret
        :param main_user_open_id: main_user_open_id
        :return app_info
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        store_user_nick = user_nick.split(':')[0]
        if not store_user_nick:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，请先授权登录"
            return invoke_result_data
        if not open_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，请先授权登录"
            return invoke_result_data
        
        base_info = BaseInfoModel(context=self.context, is_auto=True).get_dict(field="client_ver,project_ver")
        if not base_info:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "对不起，系统异常，请联系管理员"
            return invoke_result_data
        
        condition_where = ConditionWhere()
        condition_where.add_condition("store_user_nick=%s")
        params = [store_user_nick]
        template_id = share_config.get_value("client_template_id")
        if template_id:
            condition_where.add_condition("template_id=%s")
            params.append(template_id)
        app_info_model = AppInfoModel(context=self.context, is_auto=True)
        app_info = app_info_model.get_entity(condition_where.to_string(), params=params)
        top_base_model = TopBaseModel(context=self.context)
        invoke_result_data = top_base_model.get_dead_date(store_user_nick, access_token, app_key, app_secret)
        if invoke_result_data.success == False:
            return invoke_result_data
        dead_date = invoke_result_data.data
        project_code = top_base_model.get_project_code(store_user_nick,access_token,app_key, app_secret)
        now_timestamp = TimeHelper.datetime_to_timestamp(datetime.datetime.strptime(TimeHelper.get_now_format_time('%Y-%m-%d 00:00:00'), '%Y-%m-%d %H:%M:%S'))
        login_log = TaoLoginLogModel(context=self.context, is_auto=True).get_entity("open_id=%s", order_by="id desc", params=open_id)
        if app_info:
            if dead_date != "expire":
                app_info.expiration_date = dead_date
            if project_code != "":
                app_info.project_code = project_code
            invoke_result_data = top_base_model.get_shop(access_token, app_key, app_secret)
            if invoke_result_data.success == True:
                app_info.access_token = access_token
                app_info.store_name = invoke_result_data.data['shop_seller_get_response']['shop']['title']
                app_info.store_icon = invoke_result_data.data['shop_seller_get_response']['shop']['pic_path']
            if app_info.main_user_open_id != main_user_open_id:
                app_info.main_user_open_id = main_user_open_id
            app_info_model.update_entity(app_info,"expiration_date,project_code,access_token,main_user_open_id,store_name,store_icon")
            app_info_model.delete_dependency_key(DependencyKey.app_info(app_info.app_id))

            app_info.user_nick = user_nick
            app_info.dead_date = dead_date
            app_info.project_code = project_code
            if app_info.dead_date != "expire":
                dead_date_timestamp = TimeHelper.datetime_to_timestamp(datetime.datetime.strptime(app_info.dead_date, '%Y-%m-%d %H:%M:%S'))
                app_info.surplus_day = int(int(abs(dead_date_timestamp - now_timestamp)) / 24 / 3600)
            app_info.last_login_date = login_log.modify_date if login_log else ""
            app_info.template_ver = app_info.template_ver if not base_info["project_ver"] else app_info.project_ver
            invoke_result_data.data = app_info
            return invoke_result_data
        else:
            app_info = AppInfo()
            app_info.access_token = access_token
            app_info.template_ver = base_info["client_ver"] if not base_info["project_ver"] else base_info["project_ver"]
            app_info.user_nick = user_nick
            app_info.dead_date = dead_date
            app_info.project_code = project_code
            if app_info.dead_date != "expire":
                dead_date_timestamp = TimeHelper.datetime_to_timestamp(datetime.datetime.strptime(app_info.dead_date, '%Y-%m-%d %H:%M:%S'))
                app_info.surplus_day = int(int(abs(dead_date_timestamp - now_timestamp)) / 24 / 3600)
            app_info.last_login_date = login_log.create_date if login_log else ""
            invoke_result_data.data = app_info
            return invoke_result_data

    def get_online_url(self, act_id, app_id, module_id=0, act_type=0):
        """
        :description: 获取online_url
        :param act_id:活动标识
        :param app_id:应用标识
        :param module_id:模块标识
        :param act_type:活动类型
        :return str
        :last_editors: HuangJianYi
        """
        page_index = ""
        page = share_config.get_value("page_index")
        if page:
            if isinstance(page,dict):
                cur_page = page.get(str(act_type),"")
                if cur_page:
                    page_index = "&page=" + CodingHelper.url_encode(cur_page)
            else:
                page_index = "&page=" + CodingHelper.url_encode(page)
        query = CodingHelper.url_encode(f"actid={act_id}")
        if module_id > 0:
            query = CodingHelper.url_encode(f"actid={act_id}&module_id={module_id}")
        online_url = f"https://m.duanqu.com/?_ariver_appid={app_id}&_mp_code=tb&transition=present{page_index}&query={query}"
        return online_url

    def get_live_url(self, app_id):
        """
        :description: 获取live_url
        :param app_id:应用标识
        :return str
        :last_editors: HuangJianYi
        """
        live_url = f"https://market.m.taobao.com/app/taefed/shopping-delivery-wapp/index.html#/putin?mainKey=form&appId={app_id}"
        return live_url

    def _delete_dict_info_dependency_key(self, parent_id, dict_type, delay_delete_time=0.01):
        """
        :description: 删除字典信息依赖建
        :param parent_id: 父节点标识
        :param dict_type: 字典类型
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: HuangJianYi
        """
        DictInfoModel().delete_dependency_key(DependencyKey.dict_info_list(parent_id, dict_type), delay_delete_time)

    def save_dict_info(self, dict_id, parent_id, dict_type, dict_name, dict_value, dict_pic, sort_index, is_release, i1, i2, s1, s2):
        """
        :description: 保存字典
        :param dict_id: 字典标识
        :param parent_id: 父节点标识
        :param dict_type: 字典类型
        :param dict_name：字典名称
        :param dict_value：字典值
        :param dict_pic：字典图片
        :param sort_index：排序
        :param is_release：是否发布
        :param i1：i1
        :param i2：i2
        :param s1：s1
        :param s2：s2
        :return
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        if (not parent_id and not dict_type) or not dict_name:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data
        old_dict_info = None
        dict_info = None
        is_add = False
        dict_info_model = DictInfoModel(context=self.context)
        if dict_id > 0:
            dict_info = dict_info_model.get_entity_by_id(dict_id)
            if not dict_info:
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "信息不存在"
                return invoke_result_data
            old_dict_info = deepcopy(dict_info)
        if not dict_info:
            is_add = True
            dict_info = DictInfo()
        dict_info.parent_id = parent_id
        dict_info.dict_type = dict_type
        dict_info.dict_name = dict_name
        dict_info.dict_value = dict_value
        dict_info.dict_pic = dict_pic
        dict_info.sort_index = sort_index
        dict_info.is_release = is_release
        dict_info.i1 = i1
        dict_info.i2 = i2
        dict_info.s1 = s1
        dict_info.s2 = s2
        dict_info.modify_date = SevenHelper.get_now_datetime()
        if is_add:
            dict_info.create_date = dict_info.modify_date
            dict_info.id = dict_info_model.add_entity(dict_info)
        else:
            dict_info_model.update_entity(dict_info,exclude_field_list="parent_id,create_date")
        result = {}
        result["is_add"] = is_add
        result["new"] = dict_info
        result["old"] = old_dict_info
        invoke_result_data.data = result
        self._delete_dict_info_dependency_key(parent_id, dict_type)
        return invoke_result_data

    def get_dict_info_list(self, parent_id, dict_type, page_size, page_index, order_by="id desc",field="*", is_cache=True):
        """
        :description: 字典列表
        :param parent_id：父节点标识
        :param dict_type: 字典类型
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param field：查询字段
        :param is_cache：是否缓存
        :return:
        :last_editors: HuangJianYi
        """
        page_list = []
        total = 0
        if not parent_id or not dict_type:
            return page_list, total
        condition_where = ConditionWhere()
        params = []
        if parent_id:
            condition_where.add_condition("parent_id=%s")
            params.append(parent_id)
        if dict_type:
            condition_where.add_condition("dict_type=%s")
            params.append(dict_type)
        condition_where.add_condition("is_release=1")

        if is_cache == True:
            page_list, total = DictInfoModel(context=self.context, is_auto=True).get_cache_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by,params=params,dependency_key=DependencyKey.dict_info_list(parent_id,dict_type),cache_expire=600)
        else:
            page_list, total = DictInfoModel(context=self.context).get_dict_page_list(field=field, page_index=page_index, page_size=page_size, where=condition_where.to_string(), group_by="", order_by=order_by,params=params)
        return page_list, total