function NewGridMapping() {
    $("#grid").remove()
    $("#grid2").remove()
    $("#master").append(`<div id="grid"></div>`)
    
    $.ajax({
        type : "get",
        url : "/json_emp/",
        async : false,
        contentType : "application/json",
        success : function(result){  
            emp_data = result           
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    // 사원 Grid 생성
    instance_emp = new tui.Grid({
    el: document.getElementById('grid'), 
    bodyHeight: 750,
    width : 1000,
    scrollX: true,
    columns: [
        {
        header: '부서명',
        name: 'DeptName',
        width: 250,
        filter: {
            type : 'text',
            showClearBtn: true
        }  
        },
        {
        header: '사원명',
        name: 'EmpName',
        width: 200,
        filter: {
            type : 'text',
            showClearBtn: true
        }
        },
        {
        header: '사번',
        name: 'UserId',
        hidden: true
        },
        {
        header: '그룹',
        name: 'GroupSeq',
        formatter: 'listItemText',
        editor: {
            type: 'select',
            options: {
                listItems: [                  
                    {
                        text: '영업팀장',
                        value: '1'
                    },
                    {
                        text: '영업본부장',
                        value: '2'
                    },
                    {
                        text: '마케팅',
                        value: '3'
                    },
                    {
                        text: '관리부서',
                        value: '4'
                    }
                ],
                
            }
        },
        onAfterChange: (ev) => {instance_emp.setValue(ev.rowKey, 'Changed', 'U')}
        },
        {
        header: '변경',
        name: 'Changed',
        //hidden: true
        },
    ],
    data: emp_data
    });

    instance_emp.filter('EmpName', [{code : 'contain', value : ''}])
    instance_emp.filter('DeptName', [{code : 'contain', value : ''}])
}

function save() {   
    var call = new Array();
    save_xml = `N'<Root>`;
    changed = instance_emp.getColumnValues('Changed')
    for (e in changed) {
        if (changed[e] == 'U') {
            // 변경된 RowKey (sort 사용시 +1 필요)
            call.push(Number(e));
        }
    }

    for (e in call) { 
        save_xml += `<Data><UserId>${instance_emp.getData()[call[e]].UserId}</UserId><GroupSeq>${instance_emp.getData()[call[e]].GroupSeq}</GroupSeq></Data>`
    }
    save_xml += `</Root>'`

    xml = {"save_xml": save_xml}

    console.log(xml);

    $.ajax({
        type : "post",
        url : "/save_groupmapping/",
        data : JSON.stringify(xml),
        async : false,
        contentType : "application/json",
        success : function(result){  
            alert("성공");
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    $.ajax({
        type : "get",
        url : "/json_emp/",
        async : false,
        contentType : "application/json",
        success : function(result){  
            emp_data = result
            instance_emp.resetData(emp_data)
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    // 저장 후 변경분 check 초기화 및 권한 다시 조회
}