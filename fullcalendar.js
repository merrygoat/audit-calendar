import {loadResource} from "../../static/utils/resources.js";

export default {
    template: "<div></div>",
    props: {
        options: Array,
        resource_path: String,
    },
    async mounted() {
        await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
        await loadResource(window.path_prefix + `${this.resource_path}/index.global.min.js`);
        this.options.eventClick = (info) => this.$emit("click", {info});
        this.calendar = new FullCalendar.Calendar(this.$el, this.options);
        this.calendar.render();
    },
    methods: {
        update_calendar() {
            if (this.calendar) {
                this.calendar.setOption("events", this.options.events);
                this.calendar.render();
            }
        },
        get_events() {
            if (this.calendar) {
                return this.calendar.getEvents();
            }
        },
        set_event_start(id, date) {
            if (this.calendar) {
                let event = this.calendar.getEventById(id)
                event.setStart(date, {maintainDuration: true})
            }
        },
        set_event_prop(id, prop_name, prop_value) {
            if (this.calendar) {
                let event = this.calendar.getEventById(id)
                event.setProp(prop_name, prop_value)
            }
        },
        update_event(id, ) {
            if (this.calendar) {
                let event = this.calendar.getEventById(id)
                event.setProp("backgroundColor", colour)
                event.setProp("borderColor", colour)
            }
        }
    },
};