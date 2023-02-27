function query() {
    if ((typeof menuId === 'undefined') && (typeof targetseq === 'undefined')) {
    // if ((typeof menuId === 999999) && (typeof targetseq === 999999)) {        
        alert('둘다입력');
    }
    else if (typeof menuId === 'undefined') {
    // else if (typeof menuId === 999999) {        
        alert('메뉴입력');
    }
    else if (typeof targetseq === 'undefined') {
    // else if (typeof targetseq === 999999) {        
        alert('대상입력');
    }
    else {
        if (targetseq == 1) {
            tmp_menu = menuId;
            tmp_target = targetseq;
            $('#status').empty();
            $('#status').append('선택된 화면 : ' + menu_list[Number(menuId)-1].text);
            $('#status').append('</br>선택된 대상 : 사원');
            $('#detail1 div').empty();
            $('#detail2 div').empty();
            $('#setting').empty();
            //$('#setting').append('<input type="button" id= "setting1" value=">" onclick="emp1()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="emp1()">
                                    <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            //$('#setting').append('<input type="button" id= "setting2" value="<" onclick="emp2()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="emp2()">
                                    <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            emp_grid();
        }
        else if (targetseq == 2) {
            tmp_menu = menuId;
            tmp_target = targetseq;
            $('#status').empty();
            $('#status').append('선택된 화면 : ' + menu_list[Number(menuId)-1].text);
            $('#status').append('</br>선택된 대상 : 부서');
            $('#detail1 div').empty();
            $('#detail2 div').empty();
            $('#setting').empty();
            //$('#setting').append('<input type="button" id= "setting1" value=">" onclick="dept1()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="dept1()">
                                    <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            //$('#setting').append('<input type="button" id= "setting2" value="<" onclick="dept2()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="dept2()">
                                    <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            dept_grid();
        }
        else if (targetseq == 3) {
            tmp_menu = menuId;
            tmp_target = targetseq;
            $('#status').empty();
            $('#status').append('선택된 화면 : ' + menu_list[Number(menuId)-1].text);
            $('#status').append('</br>선택된 대상 : 그룹');
            $('#detail1 div').empty();
            $('#detail2 div').empty();
            $('#setting').empty();
            //$('#setting').append('<input type="button" id= "setting1" value=">" onclick="group1()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="group1()">
                                    <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            //$('#setting').append('<input type="button" id= "setting2" value="<" onclick="group2()">');
            $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="group2()">
                                    <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                                  </button>`);
            group_grid();
        }
    }
}

function refresh(tmp_menu, tmp_target) {
    if (tmp_target == 1) {
        $('#status').empty();
        $('#status').append('선택된 화면 : ' + menu_list[Number(tmp_menu)-1].text);
        $('#status').append('</br>선택된 대상 : 사원');
        $('#detail1 div').empty();
        $('#detail2 div').empty();
        $('#setting').empty();
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="emp1()">
                                <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="emp2()">
                                <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        emp_grid();
    }
    else if (tmp_target == 2) {
        $('#status').empty();
        $('#status').append('선택된 화면 : ' + menu_list[Number(tmp_menu)-1].text);
        $('#status').append('</br>선택된 대상 : 부서');
        $('#detail1 div').empty();
        $('#detail2 div').empty();
        $('#setting').empty();
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="dept1()">
                                <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="dept2()">
                                <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        dept_grid();
    }
    else if (tmp_target == 3) {
        $('#status').empty();
        $('#status').append('선택된 화면 : ' + menu_list[Number(tmp_menu)-1].text);
        $('#status').append('</br>선택된 대상 : 그룹');
        $('#detail1 div').empty();
        $('#detail2 div').empty();
        $('#setting').empty();
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting1" onclick="group1()">
                                <i class="bi bi-caret-right-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        $('#setting').append(`<button class="btn btn-outline-secondary" id= "setting2" onclick="group2()">
                                <i class="bi bi-caret-left-fill" style="font-size:1.5rem;"></i>
                              </button>`);
        group_grid();
    }
}


function save() {
    if (tmp_target == 1) { 
        save_emp()
    }
    else if (tmp_target == 2) {
        save_dept()
    }
    else if (tmp_target == 3) {
        save_group()
    }
}

function save_emp() {
    // 좌측 그리드 instance_emp1
    // 우측 그리드 instance_emp2
    var call1 = new Array();
    var call2 = new Array();
    var callmenu = Object.values(menu_list[Number(tmp_menu)-1]) // 현재 메뉴에 대한 정보 (MenuId, MenuName, Url, Sort)
    
    changed1 = instance_emp1.getColumnValues('Changed')
    changed2 = instance_emp2.getColumnValues('Changed')
    // console.log(changed);
    for (e in changed1) {
        if (changed1[e] == 'U') {
            call1.push(instance_emp1.getData()[e].UserId)
        }
    }
    for (e in changed2) {
        if (changed2[e] == 'U') {
            call2.push(instance_emp2.getData()[e].UserId)
        }
    }

    console.log(call1);
    console.log(call2);
    console.log(callmenu);

    var datals = {'call1':call1, 'call2':call2, 'callmenu':callmenu}
    
    console.log(datals);
  
    $.ajax({
        type : "post",
        url : "/save_emp/",
        traditional: true,
        async : false,
        contentType : "application/json",
        data : JSON.stringify(datals),
        success : function(result){  
            alert('저장되었습니다.');
            refresh(tmp_menu, tmp_target)
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

}
function save_dept() {
    // 좌측 그리드 instance_dept1
    // 우측 그리드 instance_dept2
    var call1 = new Array();
    var call2 = new Array();
    var callmenu = Object.values(menu_list[Number(tmp_menu)-1]) // 현재 메뉴에 대한 정보 (MenuId, MenuName, Url, Sort)
    
    changed1 = instance_dept1.getColumnValues('Changed')
    changed2 = instance_dept2.getColumnValues('Changed')
    // console.log(changed);
    for (e in changed1) {
        if (changed1[e] == 'U') {
            call1.push(instance_dept1.getData()[e].DeptSeq)
        }
    }
    for (e in changed2) {
        if (changed2[e] == 'U') {
            call2.push(instance_dept2.getData()[e].DeptSeq)
        }
    }

    console.log(call1);
    console.log(call2);
    console.log(callmenu);

    var datals = {'call1':call1, 'call2':call2, 'callmenu':callmenu}
    
    console.log(datals);
  
    $.ajax({
        type : "post",
        url : "/save_dept/",
        traditional: true,
        async : false,
        contentType : "application/json",
        data : JSON.stringify(datals),
        success : function(result){  
            alert('저장되었습니다.');
            refresh(tmp_menu, tmp_target)
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });
}
function save_group() {
    // 좌측 그리드 instance_group1
    // 우측 그리드 instance_group2
    var call1 = new Array();
    var call2 = new Array();
    var callmenu = Object.values(menu_list[Number(tmp_menu)-1]) // 현재 메뉴에 대한 정보 (MenuId, MenuName, Url, Sort)
    
    changed1 = instance_group1.getColumnValues('Changed')
    changed2 = instance_group2.getColumnValues('Changed')
    // console.log(changed);
    for (e in changed1) {
        if (changed1[e] == 'U') {
            call1.push(instance_group1.getData()[e].GroupSeq)
        }
    }
    for (e in changed2) {
        if (changed2[e] == 'U') {
            call2.push(instance_group2.getData()[e].GroupSeq)
        }
    }

    console.log(call1);
    console.log(call2);
    console.log(callmenu);

    var datals = {'call1':call1, 'call2':call2, 'callmenu':callmenu}
    
    console.log(datals);
  
    $.ajax({
        type : "post",
        url : "/save_group/",
        traditional: true,
        async : false,
        contentType : "application/json",
        data : JSON.stringify(datals),
        success : function(result){  
            alert('저장되었습니다.');
            refresh(tmp_menu, tmp_target)
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });
}

function emp_grid() {
    // Ajax 호출 후 Grid에 들어갈 데이터 변수에 담기
    $.ajax({
        type : "get",
        url : "/json_emp/",
        async : false,
        contentType : "application/json",
        success : function(result){  
            emp_data1 = result
            console.log();
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    $.ajax({
        type : "get",
        url : "/secu/emp/" + menuId,
        async : false,
        contentType : "application/json",
        success : function(result){  
            emp_data2 = result
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    // console.log(emp_data1);
    // console.log(emp_data2);

    for (i=0 ; i<emp_data2.length; i++) {
        emp_data1 = emp_data1.filter(o => o.UserId !== emp_data2[i].UserId);
    }
    
    // console.log(emp_data1);


    // Grid 생성
    instance_emp1 = new tui.Grid({
        el: document.getElementById('detail1'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        // scrollX: true,
        columns: [
            {
                header: '부서명',
                name: 'DeptName',
                width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '부서코드',
                name: 'DeptSeq',
                hidden: true
            },
            {
                header: '사원명',
                name: 'EmpName',
                filter: {type : 'text', showClearBtn: true}
            },
            {
                header: '사번',
                name: 'UserId',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: emp_data1
    });
    instance_emp1.setColumnValues('Changed', '')
    
    //instance_emp1.setHeight('1px')


    instance_emp2 = new tui.Grid({
        el: document.getElementById('detail2'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        scrollX: true,
        columns: [
            {
                header: '부서명',
                name: 'DeptName',
                width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '부서코드',
                name: 'DeptSeq',
                hidden: true
            },
            {
                header: '사원명',
                name: 'EmpName',
                filter: {type : 'text', showClearBtn: true}
            },
            {
                header: '사번',
                name: 'UserId',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: emp_data2
    });
    instance_emp2.setColumnValues('Changed', '')
    tui.Grid.applyTheme('striped'); 
}

function emp1() {
    // console.log(instance_emp1.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_emp1.getRow(instance_emp1.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_emp2.appendRow({DeptSeq : tmp.DeptSeq, DeptName : tmp.DeptName, UserId : tmp.UserId, EmpName : tmp.EmpName, Changed : 'U'})
    instance_emp1.removeRow(instance_emp1.getFocusedCell().rowKey); // 삭제
}

function emp2() {
    // console.log(instance_emp2.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_emp2.getRow(instance_emp2.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_emp1.appendRow({DeptSeq : tmp.DeptSeq, DeptName : tmp.DeptName, UserId : tmp.UserId, EmpName : tmp.EmpName, Changed : 'U'})
    instance_emp2.removeRow(instance_emp2.getFocusedCell().rowKey); // 삭제
}

function dept_grid() {
    // Ajax 호출 후 Grid에 들어갈 데이터 변수에 담기
    $.ajax({
        type : "get",
        url : "/json_dept/",
        async : false,
        contentType : "application/json",
        success : function(result){  
            dept_data1 = result
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    $.ajax({
        type : "get",
        url : "/secu/dept/" + menuId,
        async : false,
        contentType : "application/json",
        success : function(result){  
            dept_data2 = result
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    // console.log(dept_data1);
    // console.log(dept_data2);

    for (i=0 ; i<dept_data2.length; i++) {
        dept_data1 = dept_data1.filter(o => o.DeptSeq !== dept_data2[i].DeptSeq);
    }
    // console.log(dept_data1);

    // Grid 생성
    instance_dept1 = new tui.Grid({
        el: document.getElementById('detail1'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        scrollX: true,
        columns: [
            {
                header: '부서명',
                name: 'DeptName',
                // width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '부서코드',
                name: 'DeptSeq',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: dept_data1
    });

    instance_dept2 = new tui.Grid({
        el: document.getElementById('detail2'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        scrollX: true,
        columns: [
            {
                header: '부서명',
                name: 'DeptName',
                // width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '부서코드',
                name: 'DeptSeq',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: dept_data2
    });
    //instance_dept1.filter('DeptName', [{code : 'contain', value : ''}])
    tui.Grid.applyTheme('striped'); 
}

function dept1() {
    // console.log(instance_dept1.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_dept1.getRow(instance_dept1.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_dept2.appendRow({DeptSeq : tmp.DeptSeq, DeptName : tmp.DeptName, Changed : 'U'})
    instance_dept1.removeRow(instance_dept1.getFocusedCell().rowKey); // 삭제
}

function dept2() {
    // console.log(instance_dept2.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_dept2.getRow(instance_dept2.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_dept1.appendRow({DeptSeq : tmp.DeptSeq, DeptName : tmp.DeptName, Changed : 'U'})
    instance_dept2.removeRow(instance_dept2.getFocusedCell().rowKey); // 삭제
}

function group_grid() {
    // Ajax 호출 후 Grid에 들어갈 데이터 변수에 담기
    $.ajax({
        type : "get",
        url : "/json_group/",
        async : false,
        contentType : "application/json",
        success : function(result){  
            group_data1 = result
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    $.ajax({
        type : "get",
        url : "/secu/group/" + menuId,
        async : false,
        contentType : "application/json",
        success : function(result){  
            group_data2 = result
        },
        error : function(jqXHR, status, error){
            alert("알 수 없는 에러 [ " + error + " ]")
        }
    });

    // console.log(group_data1);
    // console.log(group_data2);

    for (i=0 ; i<group_data2.length; i++) {
        group_data1 = group_data1.filter(o => o.GroupSeq !== group_data2[i].GroupSeq);
    }
    // console.log(group_data1);

    // Grid 생성
    instance_group1 = new tui.Grid({
        el: document.getElementById('detail1'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        scrollX: true,
        columns: [
            {
                header: '그룹명',
                name: 'GroupName',
                // width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '그룹코드',
                name: 'GroupSeq',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: group_data1
    });

    instance_group2 = new tui.Grid({
        el: document.getElementById('detail2'), // Container element
        bodyHeight: 'fitToParent',
        // width : 760,
        scrollX: true,
        columns: [
            {
                header: '그룹명',
                name: 'GroupName',
                // width: 250,
                filter: {type : 'text', showClearBtn: true}  
            },
            {
                header: '그룹코드',
                name: 'GroupSeq',
                hidden: true
            },
            {
                header: '변경',
                name: 'Changed',
                //hidden: true
            }
        ],
        data: group_data2
    });
    //instance_dept1.filter('DeptName', [{code : 'contain', value : ''}])
    tui.Grid.applyTheme('striped'); 
}

function group1() {
    // console.log(instance_group1.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_group1.getRow(instance_group1.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_group2.appendRow({GroupSeq : tmp.GroupSeq, GroupName : tmp.GroupName, Changed : 'U'})
    instance_group1.removeRow(instance_group1.getFocusedCell().rowKey); // 삭제
}

function group2() {
    // console.log(instance_group2.getFocusedCell().rowKey); // 선택한 rowKey
    tmp = instance_group2.getRow(instance_group2.getFocusedCell().rowKey);
    // console.log(tmp);

    instance_group1.appendRow({GroupSeq : tmp.GroupSeq, GroupName : tmp.GroupName, Changed : 'U'})
    instance_group2.removeRow(instance_group2.getFocusedCell().rowKey); // 삭제
}

