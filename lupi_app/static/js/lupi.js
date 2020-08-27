Vue.component("functions", {
    template: `
        <div class="functions">
            <button @click="start()">start new round</button>
            <button @click="vote()">send vote</button>
            <button @click="stop()">stop round</button>
            <button @click="result()">get result</button>
            <button @click="rounds()">get rounds</button>
            <button @click="stat()">get stat</button>
        </div>
    `,
    methods: {
        start: function() {
            console.log("start");
            app.$refs.response.setResponse('', '');
            app.$refs.lupi_form.hide();
            app.$refs.table_view.hide();
            $.ajax({
                method: "POST",
                url: "/api/start",
                contentType: 'application/json',
                cache: false
            })
            .done(function(data, textStatus, jqXHR) {
                app.$refs.response.setResponse(jqXHR.status, jqXHR.responseText);
            })
           .fail(function(jqXHR) {
                app.$refs.response.setResponse(jqXHR.status, jqXHR.responseText);
            });
        },
        vote: function() {
            app.$refs.response.setResponse('', '');
            app.$refs.table_view.hide();
            app.func = "vote";
            app.$refs.lupi_form.show("nameAndNumber");
        },
        stop: function() {
            app.$refs.response.setResponse('', '');
            app.$refs.table_view.hide();
            app.func = "stop";
            app.$refs.lupi_form.show("roundId");
        },
        result: function() {
            app.$refs.response.setResponse('', '');
            app.$refs.table_view.hide();
            app.func = "result";
            app.$refs.lupi_form.show("roundId");
        },
        rounds: function() {
            app.$refs.response.setResponse('', '');
            app.$refs.lupi_form.hide();
            $.ajax({
                url: "/api/rounds",
                cache: false
            })
            .done(function(json) {
                app.$refs.table_view.setJsonData(json);
            });
        },
        stat: function() {
            app.$refs.response.setResponse('', '');
            app.$refs.table_view.hide();
            app.func = "stat";
            app.$refs.lupi_form.show("roundId");
        }
    }
});

Vue.component("lupi-form", {
    template: `
        <div class="lupi-form">
            <div v-show="showRoundId" class="field"><label for="round_id">Round ID:</label><input type="text" id="round_id" /></div>
            <div v-show="showName" class="field"><label for="name">Name:</label><input type="text" id="name" /></div>
            <div v-show="showNumber" class="field"><label for="number">Number:</label><input type="text" id="number" /></div>
            <button v-show="showButton" id="send" @click="send()">{{ title }}</button>
        </div>
    `,
    data() {
        return {
            showRoundId: false,
            showName: false,
            showNumber: false,
            showButton: false,
            title: ''
        }
    },
    methods: {
        show: function(v) {
            this.title = app.func;
            if(v == "roundId") {
                this.showRoundId = true;
                this.showName = false;
                this.showNumber = false;
            }
            else if(v == "nameAndNumber") {
                this.showRoundId = false;
                this.showName = true;
                this.showNumber = true;
            }
            this.showButton = true;
        },
        hide: function() {
            this.showRoundId = false;
            this.showName = false;
            this.showNumber = false;
            this.showButton = false;
        },
        send: function() {
            var method = "";
            var url = "";
            var data = undefined;
            if(app.func == "vote") {
                method = "POST";
                url = "/api/vote";
                data = {
                    name: $('#name').val(),
                    number: parseInt($('#number').val())
                };
            }
            else if(app.func == "stop") {
                method = "PUT";
                url = "/api/stop";
                data = parseInt($('#round_id').val());
            }
            else if(app.func == "result") {
                method = "GET";
                url = "/api/result/"+$('#round_id').val();
            }
            else if(app.func == "stat") {
                method = "GET";
                url = "/api/stat/"+$('#round_id').val();
            }
            $.ajax({
                method: method,
                url: url,
                data: JSON.stringify(data),
                contentType: 'application/json',
                cache: false
            })
            .done(function(data, textStatus, jqXHR) {
                if(Array.isArray(data)) {
                    app.$refs.response.setResponse(jqXHR.status, '');
                    app.$refs.table_view.setJsonData(data);
                }
                else {
                    app.$refs.response.setResponse(jqXHR.status, jqXHR.responseText);
                }
            })
           .fail(function(jqXHR) {
                app.$refs.response.setResponse(jqXHR.status, jqXHR.responseText);
            });
        }
    }
});

Vue.component("response", {
    template: `
        <div class="response">Response: {{ code }} - {{ text }}</div>
    `,
    data() {
        return {
            code: '',
            text: ''
        }
    },
    methods: {
        setResponse: function(newCode, newText) {
            this.code = newCode;
            this.text = newText
        }
    }
});

Vue.component("table-view", {
    template: `
        <div v-show="show" class="table-view">
            <table border="1" cellspacing="0" cellpadding="2">
                <tr>
                    <th v-for="th in tableHead">{{ th }}</th>
                </tr>
                <tr v-for="j in jsonData">
                    <td v-for="d in j">{{ d }}</td>
                </tr>
            </table>
        </div>
    `,
    data() {
        return {
            jsonData: {},
            tableHead: [],
            show: false
        }
    },
    methods: {
        setJsonData: function(newJsonData) {
            this.jsonData = newJsonData;
            if(this.jsonData.length > 0) {
                this.tableHead = Object.keys(this.jsonData[0]);
            }
            else {
                this.tableHead = [];
            }
            this.show = true;
        },
        hide: function() {
            this.show = false;
        }
    }
});


var app;
window.onload = function () {
    app = new Vue({
        el: "#lupi-app",
        data: {
            func: ''
        },
        methods: {

        }
    });
};
