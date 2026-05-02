class SlackMethods:
    profile_set = 'users.profile.set'
    profile_get = 'users.profile.get'
    profile_set_photo = 'users.setPhoto'
    set_sections = 'users.profile.setSections'
    users_list = 'users.list'
    users_info = 'users.info'
    users_get_presence = 'users.getPresence'

    conversations_join = 'conversations.join'
    conversations_leave = 'conversations.leave'
    conversations_list = 'conversations.list'
    conversations_open = 'conversations.open'
    conversations_history = 'conversations.history'
    conversations_replies = 'conversations.replies'
    conversations_info = 'conversations.info'

    chat_delete = 'chat.delete'
    chat_update = 'chat.update'
    chat_post_message = 'chat.postMessage'
    chat_attachments = "chat.unfurlLink"

    rtm_connect = 'rtm.connect'

    reactions_get = 'reactions.get'
    create_shared_invite = 'users.admin.createSharedInvite'
    send_invite_by_email = 'users.admin.inviteBulk'
    alternative_invite_by_email = 'users.inviteRequests.create'

    upload_file = 'files.upload'
    get_upload_url = 'files.getUploadURL'
    complete_upload = 'files.completeUpload'
    files_info = 'files.info'
    download_file = 'files.download'
    delete_file = 'files.delete'
    share_files = 'files.share'

    check_email = 'signup.checkEmail'
    confirm_email = 'signup.confirmEmail'

    confirm_code = 'signin.confirmCode'
    find_workspaces = 'signin.findWorkspaces'

    auth_test = 'auth.test'
    request_captcha = 'auth.captcha'

    team_profile_get = 'team.profile.get'
    team_info = 'team.info'
